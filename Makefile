MODE ?= prod

build-test:
	@echo "Building test mode..."
	cp .env.test .env
	docker-compose build test_db test --no-cache

test:
	@echo "Running tests in test mode..."
	cp .env.test .env
	docker-compose run --rm test

build-dev:
	@echo "Building dev mode..."
	cp .env.dev .env
	docker-compose build dev_db dev pg_admin

dev:
	@echo "Starting in dev mode..."
	cp .env.dev .env
	docker-compose up dev_db dev pg_admin

build-prod:
	@echo "Starting in prod mode..."
	cp .env.prod .env
	docker-compose build prod_db app pg_admin

prod:
	@echo "Starting in prod mode..."
	cp .env.prod .env
	docker-compose up prod_db app pg_admin

down:
	docker-compose down

logs:
	docker-compose logs -f

rebuild:
	cp .env.$(MODE) .env
	docker-compose up --build --force-recreate

