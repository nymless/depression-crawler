.PHONY: install dev build run

install:
	npm install

dev:
	npm run dev

build:
	docker build -t nymless/front-next .

run:
	docker run --rm -it --env-file=.env --add-host host.docker.internal:host-gateway -p=127.0.0.1:3000:3000 --name=front-next nymless/front-next
