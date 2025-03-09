import json
from typing import Union, Dict, Any
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Filter
from app.core.config import settings
from aiogram.filters import CommandStart
import requests

# Укажите свой токен
TOKEN = settings.BOT_TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher()

class WebAppDataFilter(Filter):
    async def __call__(self, message: types.Message, **kwds) -> Union[bool, Dict[str, Any]]:
        return dict(web_app_data=message.web_app_data) if message.web_app_data else False

def send_message_to_admins(message: str):
    chats = ["6398268582", "1372814991", "6035406614"]
    
    for id in chats:
        url = f"https://api.telegram.org/bot{settings.ADMIN_BOT_TOKEN}/sendMessage?chat_id={id}&parse_mode=markdown&text={message}"
        req = requests.get(url=url)
        print(message)
        print(req.content)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    caption = """Привет!
Мы команда профессионалов, создаём песни для героев, превращая их истории в музыку.

Вы можете подарить песню близкому на фронте или, находясь на передовой, передать его родным. Музыка навсегда увековечит историю и имя героя. 

Жми на старт – и мы создадим для вас песню"""
    photo = "https://storage.yandexcloud.net/patriot-music/svo_photo.jpg"
    adminTG = "https://t.me/PATRIOT_MNGR"
    kb = [[types.InlineKeyboardButton(text="Тех.поддержка", url=adminTG)]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb, resize_keyboard=True)
    await message.answer_photo(photo=photo, caption=caption, reply_markup=keyboard)

@dp.pre_checkout_query(lambda x: True)
async def pre_checkout_handler(query: types.PreCheckoutQuery):
    redis_client = settings.get_redis()
    payload = redis_client.get(query.invoice_payload)

    await bot.answer_pre_checkout_query(query.id, ok=True)
    @dp.message(lambda x: True)
    async def message_send(message: types.Message):
        payload_dict = json.loads(payload)
        admin_message = settings.get_application_message(data=payload_dict, type="admin")
        user_message = settings.get_application_message(data=payload_dict, type="user")
        await message.answer(user_message, parse_mode="markdown")

        send_message_to_admins(admin_message)


# async def invoice(message: types.Message, web_app_data: types.WebAppData):
#     web_app_data = json.loads(web_app_data.data)
#     price = [types.LabeledPrice(label="Pay", amount=int(web_app_data["prices"]) * 100)]
    # await bot.send_invoice(
    #     chat_id=message.chat.id,
    #     title=web_app_data["title"],
    #     description=web_app_data["description"],
    #     payload=web_app_data["payload"],
    #     currency=web_app_data["currency"],
    #     prices=price,
    #     provider_token="381764678:TEST:114933"
    # )