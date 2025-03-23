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
    TEST_REDIS_HOST: str
    TEST_REDIS_PORT: str

    BOT_TOKEN: str
    TEST_BOT_TOKEN: str

    ADMIN_BOT_TOKEN: str
    YOOKASSA_TG_API: str
    YOOKASSA_TG_TEST_API: str

    # Настройки окружения
    ENVIRONMENT: Literal["development", "production"]

    SVO_PHOTO_URL: str = "https://storage.yandexcloud.net/patriot-music/svo_photo.jpg"
    INVOICE_PHOTO_URL: str = "https://storage.yandexcloud.net/patriot-music/Frame%2095.png"

    def get_redis(self):
        return redis.Redis(
            host=f"{self.REDIS_HOST}",
            port=self.REDIS_PORT,
            decode_responses=True)

    def get_application_message(self, data: dict, type: Literal["admin", "user"]):
        if type == "admin":
            return f"""
📋 *Новая анкета*  
      Имя: {data["name"]}
      Email: {data["email"]}
      Телефон: {data["phone"]}
      Телеграм: {data["telegram"]}
      Тариф: {data["planName"]}

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
         Воспоминания о службе: {data["remembranceText"]}
         Личное обращение: {data["personalMessageText"]}
         Особые фразы: {data["specialPhrasesText"]}
         Послание в будущее: {data["futureMessageText"]}
         Другое: {data["otherText"]}
        """
        elif type == "user":
            return f"""
📋 *Ваша анкета*
      Имя: {data["name"]}
      Email: {data["email"]}
      Телефон: {data["phone"]}
      Телеграм: {data["telegram"]}
      Тариф: {data["planName"]}

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
          Воспоминания о службе: {data["remembranceText"]}
          Личное обращение: {data["personalMessageText"]}
          Особые фразы: {data["specialPhrasesText"]}
          Послание в будущее: {data["futureMessageText"]}
          Другое: {data["otherText"]}

Спасибо за ваш заказ!

Ваш заказ будет выполнен в течение 1-3 рабочих дней после оплаты.
Срок зависит от текущей загрузки.
В редких случаях выполнение может занять до 5 рабочих дней.

Если вам нужно ускорить процесс, вы можете воспользоваться услугой «Срочное выполнение» за дополнительную плату.
В этом случае мы гарантируем выполнение заказа в течение 12 часов (при условии оплаты услуги).

Если у вас остались вопросы, пожалуйста, напишите нам!
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
