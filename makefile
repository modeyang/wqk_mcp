dev:
	python server.py

save_requirement:
	pip freeze > requirements.txt


.PHONY: dev save_requirement