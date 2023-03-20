# praktikum_new_diplom
http://51.250.103.173/ 

Описание проекта:
Это мой дипломный проект при Обучении в Яндекс практикум. Для данного проекта я разарабатывал бэкенд по написаной спецификации.
Foodgram вам делится и находить новые рецепты чтобы разнообразить вашу жизнь. Сайт позволяет вам скачать список ингредеентов для рецептов, добавленых в список покупок. Так же сайт позволяет вам выбрать любимые рецепты, чтобы не потерять их и подписатья на авторов, чьи рецепты вам нравятся.
Так же вы можете делать запосы к Api. По адресу: `/api/` вы найдете все доступные пути Api.
Пример запроса Api:
Запорс:
```
http://51.250.103.173/api/tags/
```
Ответ:
```
[
    {
        "id": 1,
        "name": "tag1",
        "color": "#000001",
        "slug": "tag1"
    },
    {
        "id": 2,
        "name": "tag2",
        "color": "#fffffe",
        "slug": "tag2"
    }
]
```

Tecnhologies:
Python 3.7
Django 3.2.18
Django REST framework 3.12.4
djoser
Nginx
Docker
Postgres

# Deploy:
## Для локального запуска проекта вам необходимо:
1. На вашем компьютере должен быть установлен Docker. Если ваша операционная система Windows, вы можете установить докер десктоп, скачав дистрибутив с фоциального сайта: 
```
https://docs.docker.com/desktop/install/windows-install/
```
Подробнее об установке на любую систему можно прочесть на сайте:
```
https://docs.docker.com/get-docker/
```
2. Клонируйте проект на ваш копьютер. Через терминал это можно сделать следуюшей командой:
git clone https://github.com/Spacemarine1789/foodgram-project-react.git
3. Перейдите в терминале в папку с файлом docker-compose (foodgram-project-react/infra/) и содайте .env файл. Заполните его следуя примеру:
```
DJ_SECRET_KEY=some_string
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=***** 
DB_HOST=db 
DB_PORT=5432
```
4. Оставаясь в этой же папке выполните команду:
```
docker-compose up -d --build
```
5. После разворачивания проекта запущеные контейнеры появятся в Docker. Выполните следующие команды в терминале последовательно:
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
```
Приложение развернуто.
6. Для заполнения таблицы ингредиентов и тегов необходимо выполнить следующие команды:
```
docker-compose exec backend python manage.py loaddata ingredients2.json
docker-compose exec backend python manage.py loaddata tag2.json
```
## Для проекта на сервере вам необходимо:
1. Присоеденится к вашему серверу с локальной машины:
```
ssh <server user>@<server IP>
```
2. На вашем сервере должен быть установлены python3-pip, python3-venv и git. Если вы только развернули вашу виртуальную машину выполните последовательно следующие команды:
```
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y
```
Эти команды обновят ваш менеджер пакетов apt и установят нужные програмы.
3. кроме того на вашем сервере нужно установить docker и docker-compose:
```
sudo apt install docker
sudo apt install docker-compose
```
4. Клонируйте ваш проект на сервер:
```
git clone git@github.com:Spacemarine1789/foodgram-project-react.git
```
При это может потребоваться добавить ssh ключ вашего сервера к вашему акаунту на GitHub
5. Перейдите в папку `cd foodgram-project-react/infra` на вашем сервере и создайте .env файл:
```
touch .env
```
Заполните его даннными следуя примеру:
```
DJ_SECRET_KEY=some_string
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=***** 
DB_HOST=db 
DB_PORT=5432
```
Вы можете создать .env файл локально и отправить его на сервер с помошью scp.
6. Оставаясь в папке `foodgram-project-react/infra` выполните команду:
```
docker-compose up -d --build
```
5. После разворачивания проекта запущеные контейнеры появятся в Docker. Выполните следующие команды в терминале последовательно:
```
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
Приложение развернуто.
6. Для заполнения таблицы ингредиентов и тегов необходимо выполнить следующие команды:
```
sudo docker-compose exec backend python manage.py loaddata ingredients2.json
sudo docker-compose exec backend python manage.py loaddata tag2.json
```

# Автор:
Backend DRF написан Лаптевым Романом.
