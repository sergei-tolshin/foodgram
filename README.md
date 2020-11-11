[![foodgram Actions status](https://github.com/sergei-tolshin/foodgram-project/workflows/foodgram/badge.svg)](https://github.com/sergei-tolshin/foodgram-project/actions)

# Продуктовый помощник
Онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Демо
[http://tolshin.tk](http://tolshin.tk)
логин: demo
пароль: demo

## Подготавливаем среду для развертывания приложения

### Установка Docker

Первым шагом является установка Docker на вашем локальном компьютере или сервере:

* [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
* [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)
* [Docker for Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
* [Docker for CentOS](https://docs.docker.com/engine/install/centos/)
* [Docker for Debian](https://docs.docker.com/engine/install/debian/)

### Установка Docker Compose

Docker Compose — это дополнительный инструмент, который автоматически включается в загрузку Docker для Mac и Windows. Однако, если вы используете Linux, вам нужно будет добавить его вручную. Вы можете сделать это после завершения установки Docker, выполнив команду:

```
sudo apt-get install docker-compose
```

## Разворачиваем приложение

Клонируйте репозиторий приложения из git:

```
git clone https://github.com/sergei-tolshin/foodgram-project.git foodgram
```
Перейдите в каталог приложения:

```
cd foodgram
```

Создайте файл .env и добавьте в него переменные окружения для базы данных:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Все дальнейшие команды необходимо выполнять, находясь в каталоге приложения.

### Запускаем приложение

Запустите приложение командой: 
```
sudo docker-compose up -d
```
У вас развернётся проект, с базой данных postgres.

##### Первоначальная настройка приложения

Собираем статические файлы приложения:
```
sudo docker exec -it foodgram_web_1 python manage.py collectstatic --no-input
```
Заполняем базу начальными данными:
```
sudo docker exec -it foodgram_web_1 python manage.py loaddata fixtures.json
```
Создаем суперпользователя:
```
sudo docker exec -it foodgram_web_1 python manage.py createsuperuser
```

### Проверка работы

Наберите в адресной строке браузера адрес:
* [http://localhost/](http://localhost/) (если вы запустили приложение на локальном компьютере)
* [http://ip-адрес_сервера/](http://ip-адрес_сервера/) (если запустили приложение на сервере)

Для в хода в административну панель приложения наберите адрес [http://localhost/admin/](http://localhost/admin/) или
[http://ip-адрес_сервера/admin/](http://ip-адрес_сервера/admin/) и введите логин и пароль, созданного ранее, суперпользователя.

## Автор

**Сергей Толшин**
