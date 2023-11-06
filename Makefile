
run:
	docker compose build
	docker compose up

run-prod:
	docker compose -f docker-compose.prod.yml build
	docker compose .env -f docker-compose.prod.yml up
