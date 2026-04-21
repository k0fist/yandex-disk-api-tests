# Yandex Disk API Tests

Автотесты для API Яндекс Диска.

## Что покрыто
- получение информации о диске (GET)
- получение ссылки для загрузки файла (GET)
- загрузка файла (PUT)
- копирование файла (POST)
- удаление ресурсов (файлов) (DELETE)

## Стек
- Python
- pytest
- requests
- jsonschema
- python-dotenv

## Установка проекта, команды для git bash
1. Создания виртуального окружения - python -m venv venv
2. Активация виртуального окружения - source venv/Scripts/activate
3. Установка зависимостей - pip install -r requirements.txt
4. Создать файл с переменными окружений (.env) по шаблону файла .env.example и поместить его в корень проекта

## Запуск тестов
```Git bash
python -m pytest -v
