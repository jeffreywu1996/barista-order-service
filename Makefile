
coffee:
	@printf 'Enjoy your coffee! \xE2\x98\x95'

dev:
	@docker compose -f docker-compose.yml up --build

run:
	@docker compose -f docker-compose.yml up --build -d

down:
	@docker compose -f ./docker-compose.yml down --remove-orphans

clean: down
	@docker volume rm barista-order-service_db-postgres

shell: run
	@docker exec -it order-service bash

tests: run
	@docker exec -it order-service poetry run pytest

lint: run
	@docker exec -it order-service poetry run black .
	@docker exec -it order-service poetry run isort . --profile black

.PHONY: coffee dev run stop shell tests lint
