build-d:
	docker compose -f "docker-compose.dev.yml" -p "vk-bot" up --build -d
	make python-dev
build-p:
	docker compose -f "docker-compose.prod.yml" -p "vk-bot" up --build -d

python-dev:
	py -m app --test 1

start:
	docker compose -p "vk-bot" start

stop:
	docker compose -p "vk-bot" stop

restart: stop start

up-d:
	docker compose -f "docker-compose.dev.yml" -p "vk-bot" up -d
up-p:
	docker compose -f "docker-compose.prod.yml" -p "vk-bot" up -d

clean-data:
	docker system prune -a --volumes

make-migration:
	alembic revision --autogenerate

run-migration:
	alembic upgrade head

lint:
	mypy . --exclude=schemas/
