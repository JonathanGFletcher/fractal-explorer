FROM cupy/cupy
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY . .
RUN uv sync --frozen

EXPOSE 80
CMD ["uv", "run", "app.py"]