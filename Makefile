build:
	docker compose -f "docker-compose.prod.yml" -p "vk-bot" up --build -d

dev:
	py -m app --test 1

start:
	docker compose -p "vk-bot" start

stop:
	docker compose -p "vk-bot" stop

restart: stop start

up:
	docker compose -f "docker-compose.prod.yml" -p "vk-bot" up -d

clean-data:
	docker system prune -a --volumes

make-migration:
	alembic revision --autogenerate

run-migration:
	alembic upgrade head

lint:
	mypy . --exclude=schemas/
