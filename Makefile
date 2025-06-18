# Makefile – Atalhos para desenvolvimento e manutenção do projeto Agric
#
# Comandos principais:
#   make build      – Builda a imagem Docker de desenvolvimento
#   make up         – Sobe todos os containers (API e banco) em background
#   make updb       – Sobe apenas o container do banco de dados
#   make down       – Remove containers da API e do banco
#   make createdb   – Cria o banco de dados 'agricdb' dentro do container do Postgres
#   make migrate    – Aplica as migrações do Django
#   make seed       – Popula o banco de dados com dados iniciais
#   make run        – Inicia o servidor de desenvolvimento do Django
#   make cov        – Executa os testes do Django e gera o relatório de cobertura
#   make help       – Mostra esta ajuda

.PHONY: build up updb down createdb migrate seed run cov help

# Target: build – Builda a imagem Docker de desenvolvimento
build:
	docker build -t agric_api.dev:latest -f .devcontainer/Dockerfile .

# Target: up – Sobe todos os containers (API e banco) em background
up:
	docker-compose -f docker-compose-dev.yml up --build -d

# Target: updb – Sobe apenas o container do banco de dados
updb:
	docker-compose up -d agric_db

# Target: down – Remove containers da API e do banco
# Obs: ignora erro se o container não existir
down:
	docker rm -f agric_api.dev || true	
	docker rm -f agric_db.dev || true

# Target: createdb – Cria o banco de dados 'agricdb' dentro do container do Postgres
createdb:
	docker exec -it agric_db.dev createdb -U agric agricdb

# Target: migrate – Aplica as migrações do Django
migrate:
	docker exec -it agric_api.dev sh -c "cd /code/app && python manage.py makemigrations agric"
	docker exec -it agric_api.dev sh -c "cd /code/app && python manage.py migrate"

# Target: seed – Popula o banco de dados com dados iniciais
seed:
	docker exec -it agric_api.dev sh -c "cd /code/app && python manage.py seed"

# Target: run – Inicia o servidor de desenvolvimento do Django
run:
	docker exec -it agric_api.dev sh -c "cd /code/app && python manage.py runserver 0.0.0.0:8000"

# Target: test – Executa os testes do Django e gera o relatório de cobertura
cov:
	docker exec -it agric_api.dev sh -c "cd /code/app && pytest --cov --cov-report=html"

# Target: help – Mostra esta ajuda
help:
	@egrep "^# Target:" [Mm]akefile

# EOF
