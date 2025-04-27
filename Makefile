MODE ?= prod

up:
	@echo "Starting in $(MODE) mode..."
	cp .env.$(MODE) .env
	@echo "--- .env content ---"
	@cat .env
	docker-compose up --build

build-test:
	@echo "Running tests in test mode..."
	cp .env.test .env
	docker-compose build test --no-cache

test:
	docker-compose run --rm test

build-dev:
	@echo "Starting in dev mode..."
	cp .env.dev .env
	docker-compose build dev

dev:
	@echo "Starting in dev mode..."
	cp .env.dev .env
	@echo "--- .env content ---"
	@cat .env
	docker-compose up dev




dev:
	@echo "Starting in dev mode..."
	cp .env.dev .env
	@echo "--- .env content ---"
	@cat .env
	docker-compose run --rm dev

down:
	docker-compose down

logs:
	docker-compose logs -f

rebuild:
	cp .env.$(MODE) .env
	MODE=$(MODE) docker-compose up --build --force-recreate

