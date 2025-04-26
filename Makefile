MODE ?= prod

up:
	@echo "Starting in $(MODE) mode..."
	cp .env.$(MODE) .env
	@echo "--- .env content ---"
	@cat .env
	docker-compose up --build


down:
	docker-compose down

logs:
	docker-compose logs -f

rebuild:
	cp .env.$(MODE) .env
	MODE=$(MODE) docker-compose up --build --force-recreate

test:
	@echo "Running tests in test mode..."
	cp .env.test .env
	MODE=test pytest -v
