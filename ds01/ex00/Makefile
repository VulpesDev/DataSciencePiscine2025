all:
	@printf "Launch configuration...\n"
	@docker compose -f ./docker-compose.yml --env-file ../.env up -d

build:
	@printf "Building configuration...\n"
	@docker compose -f ./docker-compose.yml --env-file ../.env up -d --build

down:
	@printf "Stopping configuration...\n"
	@docker compose -f ./docker-compose.yml --env-file ../.env down -v

re: clean build run-scripts
	@printf "Rebuild configuration...\n"

run-scripts: 
	@printf "Running Scripts...\n"
	@bash ./automatic_table.sh && ./items_table.sh && ./truncate_tables.sh && ./populate_tables.sh

clean: down
	@printf "Cleaning configuration...\n"
	@docker system prune -a

fclean:
	@printf "Total clean of all configurations docker\n"
	@docker stop $$(docker ps -qa)
	@docker system prune --all --force --volumes
	@docker network prune --force
	@docker volume prune --force

.PHONY	: all build down re clean fclean