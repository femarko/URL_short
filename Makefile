MODE ?= prod

build:
	@echo "Building for $(MODE) mode..."
	cp .env.$(MODE) .env
	docker-compose build $(SERVICES) --no-cache

run:
	@echo "Running in $(MODE) mode..."
	cp .env.$(MODE) .env
	docker-compose up $(SERVICES)

test:
	@echo "Running tests in test mode..."
	cp .env.test .env
	docker-compose run --rm test

rebuild:
	cp .env.$(MODE) .env
	docker-compose up --build --force-recreate $(SERVICES)

down:
	docker-compose down

logs:
	docker-compose logs -f
