dev:
	uv run python server.py

save_requirement:
	uv sync 

docker-build:
	docker compose build

.PHONY: dev save_requirement docker-build