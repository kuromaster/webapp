# inti db:
python manage.py db init

# migrate db - создает файлик миграции с версией и методами upgrade и downgrade
python manage.py db migrate


# в помощь миграции - обновление таблицы и полей
python manage.py db upgrade

# ERROR
# python manage.py db migrate
# ERROR [flask_migrate] Error: Target database is not up to date.
python manage.py db stamp head
python manage.py db migrate
python manage.py db upgrade
