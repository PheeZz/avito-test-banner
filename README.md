

# Сервис баннеров Avito

## Содержание
- [Сервис баннеров Avito](#сервис-баннеров-avito)
  - [Содержание](#содержание)
  - [Описание и стек](#описание-и-стек)
  - [Запуск проекта](#запуск-проекта)
  - [Тестирование curl](#тестирование-curl)
  - [Некоторые особенности и неочевидные моменты](#некоторые-особенности-и-неочевидные-моменты)
  - [Конфигурация линтера flake8 (setup.cfg)](#конфигурация-линтера-flake8-setupcfg)
  - [Конфигурация форматтера black и isort (pyproject.toml)](#конфигурация-форматтера-black-и-isort-pyprojecttoml)
  - [Структура проекта](#структура-проекта)

## Описание и стек
Сервис представляет собой API для работы с баннерами, их тегами и фичами (целочисленные значения). Техническое задание находится в файле [task.md](./docs/task.md).<br>
Интерактивная документация API SWAGGER доступна по адресу: http://109.207.171.149:8871/ <br>
Проект реализован на следующем стеке:
- Язык программирования: Python 3.11
- Фреймворк: FastAPI
- База данных: PostgreSQL
- ORM: SqlAlchemy
- Миграции: Alembic
- Логирование: Loguru
- Валидация данных: Pydantic
- Кеширование: Redis

## Запуск проекта
1. Установить git, docker, docker-compose
2. Склонировать репозиторий
```bash
git clone https://github.com/pheezz/avito-test-banner.git
```
3. Перейти в директорию проекта
```bash
cd avito-test-banner
```
4. Запустить контейнеры
```bash
docker-compose up -d --build
```

## Тестирование curl
- Создание баннеров
<details>
    <summary><code>Баннер №1</code></summary>
Запрос:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/banner' \
  -H 'accept: application/json' \
  -H 'token: super_secret_admin_token' \
  -H 'Content-Type: application/json' \
  -d '{
  "tag_ids": [
    1
  ],
  "feature_id": 1,
  "content": {
    "title": "Скидка 50% на все товары",
    "text": "Только до конца недели...",
    "url": "https://example.com/sale"
  },
  "active": true
}'
```
Ответ:
```json
{
    "banner_id": 1
}
```
</details>
<details>
    <summary><code>Баннер №2</code></summary>
Запрос:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/banner' \
  -H 'accept: application/json' \
  -H 'token: super_secret_admin_token' \
  -H 'Content-Type: application/json' \
  -d '{
  "tag_ids": [
    2
  ],
  "feature_id": 2,
  "content": {
    "title": "Скидка 30% на определенные категории",
    "text": "Только до конца месяца...",
    "url": "https://example.com/sale"
  },
  "active": true
}'
```

Ответ:
```json
{
    "banner_id": 2
}
```

</details>

- Получение баннеров пользователем
<details>
    <summary><code>Получение баннера с тегом 1 и фичей 1</code></summary>

Запрос:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/user_banner?tag_id=1&feature_id=1&use_last_revision=false' \
  -H 'accept: application/json' \
  -H 'token: 123'
```

Ответ:
```json
{
  "title": "Скидка 50% на все товары",
  "text": "Только до конца недели...",
  "url": "https://example.com/sale"
}
```
</details>

<details>
    <summary><code>Получение баннера с тегом 2 и фичей 2</code></summary>
Запрос:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/user_banner?tag_id=2&feature_id=2&use_last_revision=false' \
  -H 'accept: application/json' \
  -H 'token: 123'
```

Ответ:
```json
{
  "title": "Скидка 30% на определенные категории",
  "text": "Только до конца месяца...",
  "url": "https://example.com/sale"
}
```
</details>


- Получение баннеров администратором
<details>
    <summary><code>Получение всех баннеров без фильтрации</code></summary>
Запрос:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/banner?limit=10&offset=0' \
  -H 'accept: application/json' \
  -H 'token: super_secret_admin_token'
```

Ответ:
```json
[
  {
    "tag_ids": [
      1
    ],
    "feature_id": 1,
    "content": {
      "title": "Скидка 50% на все товары",
      "text": "Только до конца недели...",
      "url": "https://example.com/sale"
    },
    "is_active": true,
    "banner_id": 1,
    "created_at": "2024-04-14T18:11:20.867103Z",
    "updated_at": "2024-04-14T18:11:20.867112Z"
  },
  {
    "tag_ids": [
      2
    ],
    "feature_id": 2,
    "content": {
      "title": "Скидка 30% на определенные категории",
      "text": "Только до конца месяца...",
      "url": "https://example.com/sale"
    },
    "is_active": true,
    "banner_id": 2,
    "created_at": "2024-04-14T18:11:57.705571Z",
    "updated_at": "2024-04-14T18:11:57.705594Z"
  }
]
```

</details>

<details>
    <summary><code>Получение всех баннеров с фильтрацией по тегу 1</code></summary>
Запрос:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/banner?tag_id=1&limit=10&offset=0' \
  -H 'accept: application/json' \
  -H 'token: super_secret_admin_token'
```

Ответ:
```json
[
  {
    "tag_ids": [
      1
    ],
    "feature_id": 1,
    "content": {
      "title": "Скидка 50% на все товары",
      "text": "Только до конца недели...",
      "url": "https://example.com/sale"
    },
    "is_active": true,
    "banner_id": 9,
    "created_at": "2024-04-14T18:11:20.867103Z",
    "updated_at": "2024-04-14T18:11:20.867112Z"
  }
]
```

</details>

- Обновление баннера
<details>
    <summary><code>Обновление баннера №1</code></summary>
Запрос:

```bash
curl -X 'PATCH' \
  'http://127.0.0.1:8000/banner/1' \
  -H 'accept: application/json' \
  -H 'token: super_secret_admin_token' \
  -H 'Content-Type: application/json' \
  -d '{
  "tag_ids": [
    3
  ],
  "feature_id": 2,
  "content": {
    "title": "Скидка 15% на все товары",
    "text": "Только до конца недели...",
    "url": "https://example.com/sale"
  },
  "is_active": true
}'
```

Ответ:
```text
null
```

</details>

- Получение баннера пользователем
<details>
    <summary><code>Получение баннера с тегом 3 и фичей 2</code></summary>

Запрос:
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/user_banner?tag_id=3&feature_id=2&use_last_revision=true' \
  -H 'accept: application/json' \
  -H 'token: 232'
```

Ответ:
```json
{
  "title": "Скидка 15% на все товары",
  "text": "Только до конца недели...",
  "url": "https://example.com/sale"
}
```

</details>

- Удаление баннера по id
<details>
    <summary><code>Удаление баннера №1</code></summary>

Запрос:

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/banner/1' \
  -H 'accept: */*' \
  -H 'token: super_secret_admin_token'
```

Ответ: 204 No Content

</details>

- Удаление баннера по feature_id

<details>
    <summary><code>Удаление баннера с feature_id 2</code></summary>

Запрос:

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/banner/?feature_id=2' \
  -H 'accept: */*' \
  -H 'token: super_secret_admin_token'
```

Ответ: 204 No Content

</details>

## Некоторые особенности и неочевидные моменты
1. При создании баннера, если в запросе указаны несуществующие теги или фичи, то они будут созданы автоматически. Технически это необязательно, но модели базы данных созданы так, что баннеры ссылаются на теги и фичи через внешние ключи. Поэтому, чтобы не возникало ошибок при создании баннера, было принято решение создавать теги и фичи автоматически.
2. Для отсутствия проблем с передачей объектов моделей базы данных между сессиями SqlAlchemy используется метод `session.expunge()` для удаления объектов из сессии.
3. Для удобства работы с логгером был создан кастомный логгер, который настроен на вывод в файлы логов и в stdout. Также в проекте используется middleware для логирования времени обработки запроса.
4. В проекте не предусмотрен функционал для удаления тегов и фичей, так как это не предусмотрено техническим заданием. Но при удалении баннера, если у тега или фичи нет связанных баннеров, то они удаляются автоматически.
5. В проекте не реализован функционал аутентификации и авторизации пользователей. Все запросы к API должны содержать заголовок `token`, при этом в качестве пользовательского токена можно передать любое значение, токен администратора должен быть равен `super_secret_admin_token`.
6. В большинстве большинстве случав для валидации данных используются схемы Pydantic, но в некоторых случаях валидация происходит в сервисном слое или слое зависимостей. Ошибки валидации json сопровождаются 422 статусом HTTP.
7. В случае возникновения ошибки во время выполнения запроса, клиенту возвращается json с ключом `detail` (а, не `error`), в котором содержится описание ошибки.

## Конфигурация линтера flake8 (setup.cfg)
```ini
[flake8]
exclude = .git, __pycache__, img, logs, alembic, source/database/__init__.py # Исключаемые директории
max-line-length = 100 # Максимальная длина строки
max-complexity = 15 # Максимальная комплексная сложность функций/методов
```

## Конфигурация форматтера black и isort (pyproject.toml)
```ini
[tool.isort]
profile = "black" # Профиль форматирования
line_length = 100 # Максимальная длина строки
multi_line_output = 3 # Многострочный вывод импортов (вертикальный)
include_trailing_comma = true # Добавление запятой в конце списка
use_parentheses = true # Использование скобок для многострочных списков
ensure_newline_before_comments = true # Пустая строка перед комментарием

[tool.black]
line-length = 100 # Максимальная длина строки
target-version = ["py311"] # Версия Python
include = '\.pyi?$' # Включаемые файлы (regex)
```
## Структура проекта
```ini
.
├── alembic # Директория для миграций бд
│   └── migrations
│       ├── env.py
│       ├── README
│       ├── script.py.mako
│       └── versions
│           └── 2024-04-14_init_db__0968f547eba9.py
├── alembic.ini
├── config.py # Конфигурация проекта
├── customize_logger.py # Кастомизация логгера под стиль loguru
├── docker-compose.yaml # Файл для запуска контейнеров
├── Dockerfile
├── docs
│   └── task_openapi.yml
├── logging_config.json
├── logs
├── main.py # Точка входа
├── poetry.lock
├── pyproject.toml
├── setup.cfg
└── source # Исходный код
    ├── api
    │   └── v1
    │       ├── banner
    │       │   ├── constants.py
    │       │   ├── dao.py # Data Access Object - слой для работы с базой данных
    │       │   ├── dependencies.py # Зависимости для роутера
    │       │   ├── exceptions.py # Исключения
    │       │   ├── models.py # Модели SqlAlchemy
    │       │   ├── router.py # Роутер
    │       │   ├── schemas.py # Схемы Pydantic
    │       │   └── service.py # Сервисный слой
    │       └── set_header
    │           ├── constants.py
    │           └── router.py
    ├── database
    │   ├── base_orm.py
    │   ├── custom_data_types.py
    │   ├── engine.py
    │   └── __init__.py
    └── middleware
        └── request_process_time_log.py # Middleware для логирования времени обработки запроса
```