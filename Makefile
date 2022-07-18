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
	@sudo systemctl restart docker.service
	@sudo docker-compose -f deployment/docker-compose.yml up

help: ## Display the list of make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
