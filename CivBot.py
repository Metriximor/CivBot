import configparser
import os
import re
import time
import discord
import asyncio
from discord.ext import commands
from discord import Message
from cogs.TextMeme import TextMeme
from cogs.MiscUtilities import MiscUtilities
from discord.ext.commands import Context


prefix = "%"

intents = discord.Intents.default()
intents.message_content = True  # Needed if your bot reads message content

bot = commands.Bot(
    command_prefix=prefix, description="CivBot", help_command=None, intents=intents
)


gnu_linux = """
I'd just like to interject for a moment. What you're referring to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.

Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called "Linux", and many of its users are not aware that it is basically the GNU system, developed by the GNU Project.

There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine's resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called "Linux" distributions are really distributions of GNU/Linux.
""".strip()
do_orange_response = False
# cut down on spam: don't respond if last response was recent
GNU_LINUX = "gnu_linux"
last_times: dict[str, float] = {}


@bot.command(pass_context=True)
async def invite(ctx: Context):
    """CivBot invite"""
    await ctx.channel.send(
        "https://discordapp.com/api/oauth2/authorize?client_id=614086832245964808&permissions=0&scope=bot"
    )


@bot.event
async def on_message(msg: Message):
    try:
        if msg.author.bot:
            return  # ignore self

        if len(msg.content) != 0 and msg.content.startswith(prefix):
            await bot.process_commands(msg)
            return

        lower_content = msg.content.lower()
        if "delusional" in lower_content:
            await msg.channel.send(
                "Edit CivWiki <https://civwiki.org/wiki/CivWiki:Editing_Guide>"
            )

        if "lusitanian" in lower_content:
            await msg.channel.send(file=discord.File("resources/ImageMeme/Lusitan.png"))

        if "his final message" in lower_content:
            await msg.channel.send("To live as a septembrian, is to embrace death.")
        if (
            "linux" in lower_content
            and "gnu" not in lower_content
            and time.time() - last_times.get(GNU_LINUX, time.time()) >= 60
        ):
            last_times[GNU_LINUX] = time.time()
            await msg.channel.send(gnu_linux)

        match_page = r"\[{2}([^\]\n]+) *\]{2}"
        match_template = r"\{{2}([^\]\n]+) *\}{2}"

        wiki_message = ""
        wiki_link = "https://civwiki.org/wiki/"

        pages = list(set(re.findall(match_page, msg.content)))
        templates = list(set(re.findall(match_template, msg.content)))
        for template in templates:
            pages.append("Template:" + template)
        for page in pages[:10]:
            wiki_message += wiki_link + page.replace(" ", "_") + "\n"
        if len(pages) > 0:
            await msg.channel.send(wiki_message)
        if len(msg.attachments) != 0:
            for x in msg.attachments:
                if (
                    os.path.splitext(x.filename)[1] == ".schematic"
                    or os.path.splitext(x.filename)[1] == ".schem"
                ):
                    misc_utilities: MiscUtilities = bot.get_cog("MiscUtilities")
                    if misc_utilities is not None:
                        await misc_utilities.getschematic(msg, x)
    except Exception as e:
        print(f"{msg.author}: {msg.content} failed with {e}")


@bot.event
async def on_ready():
    print("connected to discord")
    print("In " + str(len(bot.guilds)) + " guilds")
    for guild in bot.guilds:
        print("    " + guild.name)
    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game("reddit.com/r/civclassics")
    )
    registered_cmds = await bot.tree.fetch_commands()
    local_cmds = {cmd.name for cmd in bot.tree.get_commands()}
    for cmd in registered_cmds:
        if cmd.name not in local_cmds:
            print(f"Deleting unregistered command: {cmd.name}")
            bot.tree.remove_command(cmd.name, type=discord.AppCommandType.chat_input)
    await bot.tree.sync()
    print("Slash command cleanup complete.")
    print(f"Loaded cogs: {bot.cogs}")


extensions = ["ImageMeme", "TextMeme", "MiscUtilities", "CivDiscord"]


async def run_bot(token: str):
    for extension in extensions:
        await bot.load_extension(f"cogs.{extension}")
    await bot.start(token)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config_type = "auth"
    config.read("config.ini")
    token = config.get(config_type, "token")

    asyncio.run(run_bot(token))
