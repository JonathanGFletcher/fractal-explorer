FROM cupy/cupy
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y python3-opencv

WORKDIR /app

COPY . .
RUN uv sync --frozen

EXPOSE 80
CMD ["uv", "run", "app.py"]