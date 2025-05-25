dev:
	python server.py

save_requirement:
	pip freeze > requirements.txt

docker-build:
	docker compose build

.PHONY: dev save_requirement docker-build