

.PHONY: up down run stop build updb help


# Target: up - Starts the FactoryDash development environment using Docker Compose.
# Builds images if necessary and runs containers in detached mode.
#
# Usage: make up
up:
	docker-compose -f docker-compose-dev.yaml up --build -d


# Target: down - Stops and removes all containers associated with the FactoryDash development environment. 
# This includes the main application, Celery worker, Celery beat, Redis, and Postgres containers.
# The `|| true` ensures that the command doesn't fail if a container doesn't exist.
#
# Usage: make down
down:
	docker rm -f factorydash.dev || true
	docker rm -f factorydash.celery_worker.dev || true
	docker rm -f factorydash.celery_beat.dev || true
	docker rm -f factorydash.redis.dev || true
	docker rm -f factorydash.postgres.dev || true


# Target: run - Executes the 'supervisord' process within the 'factorydash.dev' container. 
# This is typically used to start and manage the application's processes within the container.
# It uses the supervisord configuration file located at 
# '/factorydash/.devcontainer/supervisord.dev.conf'.
#
# Usage: make run
run:
	docker exec factorydash.dev supervisord -c /factorydash/.devcontainer/supervisord.dev.conf


# Target: stop - Stops the 'supervisord' process within the 'factorydash.dev' container. 
# This effectively stops all processes managed by supervisord within the container.
#
# Usage: make stop
stop:
	docker exec factorydash.dev pkill supervisord




build:
	docker build -t agric_devcontainer:latest -f .devcontainer/Dockerfile .

updb:
	docker-compose up -d agric_db


# Target: help - Displays a list of available targets defined in this Makefile.
# It parses the Makefile and extracts lines that start with
# "# Target:" to provide a concise overview of available commands.
#
# Usage: make help
help:
	@egrep "^# Target:" [Mm]akefile


# EOF
