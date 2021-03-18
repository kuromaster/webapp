# inti db:
python manage.py db init

# migrate db - создает файлик миграции с версией и методами upgrade и downgrade
python manage.py db migrate


# в помощь миграции - обновление таблицы и полей
python manage.py db upgrade
