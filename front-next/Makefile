.PHONY: install
install:
	npm install

.PHONY: dev
dev:
	npm run dev

.PHONE: build
build:
	docker build -t nymless/front-next .

.PHONE: run
run:
	docker run --rm -it --env-file=.env -p=3000:3000 --name=front-next nymless/front-next
