FROM python:3.13-slim

WORKDIR /app

# Install poetry and virtual environment
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.in-project false
RUN poetry install --no-root --no-directory --no-interaction --no-cache --no-ansi --only main

COPY . .

# Describe which port the application is listening on
EXPOSE 8000

ENTRYPOINT ["poetry", "run", "uvicorn", "src.api.api:app"]
CMD ["--host", "0.0.0.0", "--port", "8000"]
