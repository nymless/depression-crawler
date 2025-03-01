.PHONY: serve
serve:
	uv run uvicorn src.api.api:app --host 0.0.0.0 --port 8000

.PHONY: build
build:
	docker build -t nymless/crawler-vk .

.PHONY: run
run:
	docker run --rm -it --env-file=.env --add-host host.docker.internal:host-gateway -p=127.0.0.1:8000:8000 --name=crawler-vk nymless/crawler-vk
