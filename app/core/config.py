from typing import Literal
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os
import redis


class Settings(BaseSettings):
    def __init__(self, **kwargs):
        os.environ.clear()
        super().__init__(**kwargs)

    # Настройки базы данных
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # Настройки пула соединений
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800
    DB_ECHO: bool = False

    REDIS_HOST: str
    REDIS_PORT: int

    BOT_TOKEN: str

    ADMIN_BOT_TOKEN: str

    # Настройки окружения
    ENVIRONMENT: str = "development"

    def get_redis(self):
        return redis.Redis(host=self.REDIS_HOST, port=self.REDIS_PORT, decode_responses=True)

    def get_application_message(self, data: dict, type: Literal["admin", "user"]):
        if type == "admin":
            return f"""
📋 *Новая анкета*  
      Имя: {data["name"]}
      Email: {data["email"]}
      Телефон: {data["phone"]}
      Телеграм: {data["telegram"]}

      • Кто заполняет форму: {data["formRole"]}  
      • Для кого создаётся песня: {data["songFor"]}  
      
      *О герое*  
      1. Имя и позывное: {data["heroName"]}  
      2. Родина: {data["heroOrigin"]}  
      3. Особая вещь/символ: {data["heroItem"]}  
      
      *О службе*  
      4. Чем занимается на передовой: {data["job"]}  
      5. Техника/оружие: {data["equipment"]}  
      
      *О характере, мотивации и команде*  
      6. Что даёт силу и мотивацию: {data["motivation"]}  
      7. Боевые товарищи: {data["comrades"]}  
      
      *Личное послание в песню*  
      8. Моменты из жизни героя: {data["moments"]}  
      9. Важные слова или цитаты: {data["words"]}  
      10. Дополнительно: 
         Воспоминания о службе: {data["additionalChecks"]["remembrance"]}
         Личное обращение: {data["additionalChecks"]["personalMessage"]}
         Особые фразы: {data["additionalChecks"]["specialPhrases"]}
         Послание в будущее: {data["additionalChecks"]["futureMessage"]}
         Другое: {data["otherText"]}
        """
        elif type == "user":
            return f"""
📋 *Ваша анкета*  
      Имя: {data["name"]}
      Email: {data["email"]}
      Телефон: {data["phone"]}
      Телеграм: {data["telegram"]}

      • Кто заполняет форму: {data["formRole"]}  
      • Для кого создаётся песня: {data["songFor"]}  
      
      *О герое*  
      1. Имя и позывное: {data["heroName"]}  
      2. Родина: {data["heroOrigin"]}  
      3. Особая вещь/символ: {data["heroItem"]}  
      
      *О службе*  
      4. Чем занимается на передовой: {data["job"]}  
      5. Техника/оружие: {data["equipment"]}  
      
      *О характере, мотивации и команде*  
      6. Что даёт силу и мотивацию: {data["motivation"]}  
      7. Боевые товарищи: {data["comrades"]}  
      
      *Личное послание в песню*  
      8. Моменты из жизни героя: {data["moments"]}  
      9. Важные слова или цитаты: {data["words"]}  
      10. Дополнительно: 
         Воспоминания о службе: {data["additionalChecks"]["remembrance"]}
         Личное обращение: {data["additionalChecks"]["personalMessage"]}
         Особые фразы: {data["additionalChecks"]["specialPhrases"]}
         Послание в будущее: {data["additionalChecks"]["futureMessage"]}
         Другое: {data["otherText"]}
        """
    def generate_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        cache_strings=False
    )


settings = Settings()
