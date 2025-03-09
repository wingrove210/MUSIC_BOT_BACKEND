FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.4.15 /uv /bin/uv

# Place executables in the environment at the front of the path
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"

# Копируем только файлы, необходимые для установки зависимостей
COPY ./pyproject.toml ./uv.lock /app/

# Устанавливаем зависимости
RUN uv sync

# Копируем остальные файлы проекта
COPY ./alembic.ini ./main.py /app/
COPY ./uploads/ /app/uploads
COPY ./alembic/ /app/alembic
COPY ./app /app/app


# По умолчанию используем uvicorn с hot-reload
CMD ["uv", "run", "main.py"]