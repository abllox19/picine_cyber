COMPOSE = docker compose

.PHONY: all up down clean logs sh

all: up

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

clean:
	$(COMPOSE) down -v --remove-orphans

logs:
	$(COMPOSE) logs -f dvwa

sh:
	$(COMPOSE) exec dvwa bash