'''
Здесь пишем пути к папкам, порты, URL интеграций и прочие настройки
важно: В микросервисах все параметры должны читаться из переменных окружения (.env).
вот пример:

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Document Generator Service"
    TEMPLATES_DIR: str = "./templates"
    OUTPUT_DIR: str = "./tmp/output"
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
'''
