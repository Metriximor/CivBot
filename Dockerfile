FROM astral/uv:latest
WORKDIR /app
COPY . /app
RUN uv sync
CMD ["uv", "run", "CivBot.py"]
