.PHONY: clean-force
clean-force:
	docker rm -f $(docker ps -aq) | true
	docker image rm -f filler

.PHONY: clean
clean:
	docker rm -f $(docker ps -aq) | true

.PHONY: build
build:
	docker build --tag filler filler
	docker build --tag flask_app flask_app

.PHONY: reload
reload: clean compose

.PHONY: compose
compose:
	docker-compose up

.PHONY: lint
lint:
	black -l 120 -S .
