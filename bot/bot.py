import json
from typing import Union, Dict, Any
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Filter
from app.core.config import settings
from aiogram.filters import CommandStart
import aiohttp
import asyncio

import logging
logging.basicConfig(level=logging.INFO)


bot = Bot(settings.TEST_BOT_TOKEN if settings.ENVIRONMENT == "development" else settings.BOT_TOKEN)
dp = Dispatcher()

def get_redis_data(key):
    redis_client = settings.get_redis()
    payload = redis_client.get(key)
    if not payload:
        return None
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON для ключа {key}")
        return None
    

class WebAppDataFilter(Filter):
    async def __call__(self, message: types.Message, **kwds) -> Union[bool, Dict[str, Any]]:
        return dict(web_app_data=message.web_app_data) if message.web_app_data else False

async def send_message_to_admins(message: str):
    chats = ["6398268582", "1372814991", "6035406614", "251173063"]
    url = f"https://api.telegram.org/bot{settings.ADMIN_BOT_TOKEN}/sendMessage"

    async with aiohttp.ClientSession() as session:
        tasks = [
            session.get(url, params={"chat_id": chat_id, "parse_mode": "markdown", "text": message})
            for chat_id in chats
        ]
        await asyncio.gather(*tasks)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    caption = (
        "Привет!\n"
        "Мы команда профессионалов, создаём песни для героев, превращая их истории в музыку.\n\n"
        "Вы можете подарить песню близкому на фронте или, находясь на передовой, передать его родным. "
        "Музыка навсегда увековечит историю и имя героя.\n\n"
        "Жми на старт – и мы создадим для вас песню."
    )
    photo = settings.SVO_PHOTO_URL
    adminTG = "https://t.me/PATRIOT_MNGR"
    comments_tg = "https://t.me/patriotComments"
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="Тех.поддержка", url=adminTG)], 
                         [types.InlineKeyboardButton(text="Комментарии", url=adminTG)]]
    )
    await message.answer_photo(photo=photo, caption=caption, reply_markup=keyboard)


@dp.pre_checkout_query()
async def pre_checkout_handler(query: types.PreCheckoutQuery):
    logging.info(f"Получен pre_checkout запрос от {query.from_user.id}: {query.invoice_payload}")
    await query.answer(ok=True)
            
@dp.message(F.successful_payment)
async def message_send(message: types.SuccessfulPayment):
    try:
        data = get_redis_data(message.successful_payment.invoice_payload)
        if data is None:
            logging.warning(f"Не удалось получить данные из Redis: {message.successful_payment.invoice_payload}")
            return 

        logging.info(f"Успешный платеж: {data}")
        admin_message = settings.get_application_message(data=data, type="admin")
        user_message = settings.get_application_message(data=data, type="user")

        await message.answer(user_message, parse_mode="markdown")
        await send_message_to_admins(admin_message)

    except Exception as e:
        logging.error(f"Ошибка обработки платежа: {e}")