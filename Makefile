.PHONY: dev run

dev:
	docker compose -f docker-compose.dev.yml build
	docker compose -f docker-compose.dev.yml up --watch

run:
	docker compose build
	docker compose up