run:
	@python manage.py runserver 8002

test:
	@pytest -s

migrate:
	@python manage.py makemigrations
	@python manage.py migrate

clean:
	@find . -name *.pyc -delete
	
up:
	@docker-compose -f ./dockerize/docker-compose.yml up -d

down:
	@docker-compose -f ./dockerize/docker-compose.yml down 

reset: down up

stop: 
	@docker-compose -f ./dockerize/docker-compose.yml stop

build: 
	@docker-compose -f ./dockerize/docker-compose.yml build 

rebuild: 
	@docker-compose -f ./dockerize/docker-compose.yml build --no-cache

bootstrap: migrate
	@python manage.py load_fixtures
	
