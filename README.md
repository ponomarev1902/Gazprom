# Gazprom
## Предварительные требования

Установленный Docker 
### Установка
Для установки приложения достаточно клонировать данный проект, перейти в папку с проектом, которая содержит файл docker-compose.yml и выполнить команду 

```docker compose up --build```

После старта проекто и перед его использованием, необходимо выполнить следующие команды:

```docker compose exec web python manage.py makemigrations```
```docker-compose exec web python manage.py migrate```

Затем в браузере открыть ссылку [http://127.0.0.1:8000/report/upload/](url)
