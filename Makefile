.PHONY: dev run

dev:
	docker compose build
	docker compose up

run:
	docker compose -f docker-compose.prod.yml build
	docker compose -f docker-compose.prod.yml up
