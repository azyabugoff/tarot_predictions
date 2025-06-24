.PHONY: install test run dev clean deploy

# Development commands
install:
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v --cov=. --cov-report=html

run:
	python app.py

dev:
	export FLASK_ENV=development && python app.py

# Production commands
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov

# Render deployment (free tier optimized)
deploy:
	gunicorn --bind 0.0.0.0:10000 --workers 1 --timeout 300 --keep-alive 2 "app:create_app()"

# Alternative deployment command for Render (free tier)
start:
	gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --keep-alive 2 "app:create_app()" 