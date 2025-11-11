Создание и тестирование АРМ работника стационара больницы (учет пациентов стационара больницы)
Приложение, предназначенное для обработки данных о пациентах стационара больницы.

# Название проекта
hospital_api

# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Установка зависимостей с локального репозитория
pip install --no-index --find-links=\\172.30.44.161\public python-dotenv, psycopg2, sqlmodel, fastapi, pydantic, python-dotenv, uvicorn, argon2_cffi, passlib, fastapi-pagination, python-jose, sqlalchemy

# Запуск приложения с сетью
uvicorn app.main:app_v1 --reload

# Запуск приложения без сети
uvicorn app.main:app_v2 --reload