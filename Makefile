setup: requirements.txt
	pip install -r requirements.txt
run:
	# uvicorn main:app --reload --port=8080
	python src/run.py
clean:
	rm -rf __pycache__