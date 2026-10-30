FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY . .

RUN pip install uv

RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "python", "main.py"]