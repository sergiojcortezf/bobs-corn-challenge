# Comandos para Docker
build:
	docker compose up --build

up:
	docker compose up

down:
	docker compose down

# Comandos dentro del contenedor
test:
	docker compose exec web python manage.py test core

migrate:
	docker compose exec web python manage.py migrate

format:
	docker compose exec web black .

superuser:
	docker compose exec web python manage.py createsuperuser

# Limpieza
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +