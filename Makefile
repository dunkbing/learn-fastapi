DOCKER_IMAGE=learn-fastapi

setup: requirements.txt
	pip install -r requirements.txt
run:
	# uvicorn main:app --reload --port=8080
	python src/run.py
docker-build:
	docker build -t $(DOCKER_IMAGE) .
clean:
	rm -rf __pycache__