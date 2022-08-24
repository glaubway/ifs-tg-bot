PROJECT_NAME=ifs-tg-bot
COMPOSE=$(shell docker compose version 2>/dev/null >/dev/null && echo docker compose || echo docker-compose)
DOCKER=$(shell docker 2>/dev/null >/dev/null && echo docker || exit 1) 
TAG=$(shell git rev-parse --short HEAD)

.PHONY: build up start down destroy stop restart test

build: 
		@TAG=$(TAG) $(COMPOSE) --profile build -p $(PROJECT_NAME) build
up:
		@TAG=$(TAG) $(COMPOSE) --profile build -p $(PROJECT_NAME) up -d
rebuild:
		@make -s down
		@make -s build
		@make -s up
down:
		@TAG=$(TAG) $(COMPOSE) --profile build -p $(PROJECT_NAME) down
destroy:
		@TAG=$(TAG) $(COMPOSE) --profile build -p $(PROJECT_NAME) down -v
stop:
		@TAG=$(TAG) $(COMPOSE) --profile build -p $(PROJECT_NAME) stop
restart:
		@TAG=$(TAG) $(COMPOSE) --profile build -p $(PROJECT_NAME) stop
		@TAG=$(TAG) $(COMPOSE) --profile build -p $(PROJECT_NAME) up -d
test:
		@TAG=$(TAG) $(COMPOSE) --profile tests -p $(PROJECT_NAME)-tests build
		@TAG=$(TAG) $(COMPOSE) --profile tests -p $(PROJECT_NAME)-tests up -d
		$(DOCKER) logs -f $(PROJECT_NAME)-tests-ifstgbot-tests-1
