FROM python:3.12-alpine

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.6.0 /uv /uvx /bin/

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen

# Describe which port the application is listening on
EXPOSE 8000

# Run uvicorn server on localhost:8000
CMD ["uv", "run", "uvicorn", "src.api.api:app", "--host", "0.0.0.0", "--port", "8000"]
