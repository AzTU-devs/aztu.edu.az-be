SHELL := /bin/bash
APP_DIR := /home/projects/aztu-backend/aztu.edu.az-be
BRANCH := main

.PHONY: help pull pull-hard restart build up deploy status logs

help:
	@echo "Targets:"
	@echo "  make pull       - git pull (can fail on servers)"
	@echo "  make pull-hard  - fetch + hard reset to origin/$(BRANCH) (recommended)"
	@echo "  make restart    - docker compose restart"
	@echo "  make up         - docker compose up -d"
	@echo "  make build      - docker compose up -d --build"
	@echo "  make deploy     - pull-hard + build"
	@echo "  make status     - docker compose ps"
	@echo "  make logs       - docker compose logs -f --tail=100"

pull:
	cd $(APP_DIR) && git pull

pull-hard:
	cd $(APP_DIR) && \
	git fetch --all --prune && \
	git reset --hard origin/$(BRANCH) && \
	git clean -fd

restart:
	cd $(APP_DIR) && docker compose restart

up:
	cd $(APP_DIR) && docker compose up -d

build:
	cd $(APP_DIR) && docker compose up -d --build

deploy: pull-hard build
	@echo "✅ Backend updated, rebuilt, and restarted successfully."