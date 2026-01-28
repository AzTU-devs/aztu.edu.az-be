SHELL := /bin/bash
APP_DIR := /home/projects/aztu-backend/aztu.edu.az-be

.PHONY: pull restart deploy status logs

# Git pull
pull:
	cd $(APP_DIR) && git pull

# Restart containers (data itmir)
restart:
	cd $(APP_DIR) && docker-compose restart

# Pull + Restart (1 komanda)
deploy: pull restart
	@echo "✅ Backend updated and restarted successfully."

# Status yoxla
status:
	cd $(APP_DIR) && docker-compose ps

# Loglara bax
logs:
	cd $(APP_DIR) && docker-compose logs -f --tail=100
