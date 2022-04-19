# infra_sp2

Проект реализован для публикации рецептов. Авторизованные пользователи могут подписываться на понравившихся авторов,
добавлять рецепты в избранное, в покупки, скачать список покупок.

## Technologies

- [Python](https://www.python.org/) - programming language in this project
- [Django](https://www.djangoproject.com/) - framework for web aplications
- [PostgreSQL](https://www.postgresql.org/) - database, where we store all data
- [Gunicorn](https://gunicorn.org/) - web server for python applications
- [Nginx](https://www.nginx.com/) - we use Nginx to send static files and proxy requests to our main server
- [Docker](https://www.docker.com/) - we use it to launch all our applications in different containers

## How to install
To clone this repo you can use git clone
```
ssh: git clone git@github.com:EkaterinaSlotina/foodgram-project-react.git
https://github.com/EkaterinaSlotina/foodgram-project-react.git
```

To install docker on your system you can follow this [link](https://docs.docker.com/get-docker/)

To launch the project you need to create **.env** file
**.env** file tempate should be structured like

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME={your_database}
POSTGRES_USER={database_username}
POSTGRES_PASSWORD={databes_password}
DB_HOST=db
DB_PORT={database_port}
```

## First launch
To launch the project you need to execut this command in your terminal:

```
docker-compose up --build -d
```

If you launch the project for the first time, you need to execute this command after launching docker-compose to fulfill basic requirements of the django project:

```
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
### Workflow status
![foodgram_workflow](https://github.com/EkaterinaSlotina/foodgram-project-react/actions/workflows/main.yaml/badge.svg)

## You can see project here:
[My project](http://51.250.31.237/)

Author: Ekaterina Slotina
