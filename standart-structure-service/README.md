# Шаблон микросервисов

**эталонная структура**

```
my_microservice/
├── app/
│   ├── api/                  # HTTP-слой, эндпоинты
│   │   ├── v1/
│   │   │   ├── endpoints/    # Конкретные маршруты (templates.py, health.py ...)
│   │   │   └── router.py     # Сборщик всех маршрутов версии v1
│   ├── core/                 # Конфигурация и глобальные утилиты
│   │   ├── config.py         # Настройки (Pydantic Settings)
│   │   └── exceptions.py     # Кастомные исключения
│   ├── schemas/              # Pydantic-схемы (DTO для валидации / сериализации)
│   │   └── document.py
│   ├── services/             # Бизнес-логика (чистый Python, без привязки к FastAPI)
│   │   └── document_service.py
│   ├── storage/              # Работа с I/O (БД, S3, локальные файлы)
│   │   └── template_storage.py
│   ├── dependencies.py       # Внедрение зависимостей (FastAPI Depends)
│   └── main.py               # Точка входа, инициализация FastAPI app
├── tests/                    # Юнит- и интеграционные тесты
├── Dockerfile
├── requirements.txt / pyproject.toml
└── .env
```
