.PHONY: dev run run-cuda

dev:
	docker compose build
	docker compose up

run:
	docker compose -f docker-compose.prod.yml build
	docker compose -f docker-compose.prod.yml up

run-cuda:
	docker compose -f docker-compose.cuda.yml build
	docker compose -f docker-compose.cuda.yml up