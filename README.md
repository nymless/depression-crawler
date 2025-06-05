# Depression Crawler / Краулер депрессии

Practical part of the master’s thesis: a social media crawler that collects textual data for depression analysis.

## Thesis

Jupyter experiments for the master’s thesis are available in the repository: [depression-analysis](https://github.com/nymless/depression-analysis)

## Development

### Backend (crawler)

1. Install a dependency manager, e.g. [uv](https://docs.astral.sh/uv/getting-started/installation/).
1. From the project root, go to the crawler directory: `cd crawler-vk`
1. Copy the environment file: `cp .env.example .env`
1. Open `.env` and provide your data: tokens, keys, and other settings
1. Install dependencies: `uv sync` or `make install`
1. Run the development server on localhost: `make serve`
1. Build the Docker image: `make build`
1. Run the Docker container: `make run`

### Frontend

1. Install Node.js and NPM.
1. From the project root, go to the frontend directory: `cd front-next`
1. Copy the environment file: `cp .env.example .env`
1. Open `.env` and provide your data
1. Install dependencies: `npm install` or `make install`
1. Run the development server on localhost: `make dev`
1. Build the Docker image: `make build`
1. Run the Docker container: `make run`

## Deployment via Docker Compose

1. In the project root, copy the environment file: `cp .env.example .env`
1. Open `.env` and provide the required values
1. Build all Docker images: `make build`
1. Start all services: `make run`
1. Stop all services: `make stop`

---

Версия на русскоя языке: [README.ru.md](README.ru.md).
