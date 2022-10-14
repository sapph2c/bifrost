.PHONY: init test dev deploy help

.DEFAULT_GOAL := help

init: ## Install python dependencies
	@pip3 install -r requirements.txt

test: ## Run unit and functional tests
	@py.test tests

dev: ## Create a dev environment from the Pipfile
	@pip3 install pipenv
	@pipenv shell

deploy: ## Deploy the C2 and proxy server
	@sudo docker compose -f deployment/docker-compose.yml up

build: ## Build the docker containers and deploy
	@sudo docker compose -f deployment/docker-compose.yml build
	@sudo docker compose -f deployment/docker-compose.yml up

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
