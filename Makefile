# Makefile – Atalhos para desenvolvimento e manutenção do projeto Agric
#
# Comandos principais:
#   make build      – Builda a imagem Docker de desenvolvimento
#   make up         – Sobe todos os containers (API e banco) em background
#   make updb       – Sobe apenas o container do banco de dados
#   make down       – Remove containers da API e do banco
#   make createdb   – Cria o banco de dados 'agricdb' dentro do container do Postgres
#   make help       – Mostra esta ajuda

.PHONY: build updb createdb help

# Target: build – Builda a imagem Docker de desenvolvimento
build:
	docker build -t agric_devcontainer:latest -f .devcontainer/Dockerfile .

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

# Target: help – Mostra esta ajuda
help:
	@egrep "^# Target:" [Mm]akefile

# EOF
