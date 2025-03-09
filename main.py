import asyncio
import os
from bot.bot import bot, dp


async def start_server():
    from uvicorn import Config, Server
    config = Config("app.app:app", port=8000, host="0.0.0.0", reload=True)
    server = Server(config)
    await server.serve()

async def start_bot():
    await dp.start_polling(bot)


async def main():
    os.environ.clear()
    # Запуск бота
    task1 = asyncio.create_task(start_bot())
    task2 = asyncio.create_task(start_server())
    await asyncio.gather(task1, task2)
    

if __name__ == "__main__":
    # if settings.ENVIRONMENT == "local":
    #     print(settings.BOT_TOKEN)
    # else:
    #     print("It's production")
    asyncio.run(main())
