include .env

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the stuff
	@poetry install
	@poetry run pre-commit install
	@poetry run pre-commit autoupdate


.PHONY: flake8
flake8: ## Flake8
	@poetry run flake8

test: flake8 ## Make test

run: ## Run cron
	@poetry run python start.py
