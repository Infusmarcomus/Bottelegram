import sys
import os
import asyncio

from dotenv import load_dotenv

load_dotenv()
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers.registration import router as registration_router
from bot.handlers.common import router as common_router
from bot.handlers.messages import router as messages_router

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    if not BOT_TOKEN:
        print("Ошибка: BOT_TOKEN не установлен!")
        return

    # Добавляем storage для FSM
    storage = MemoryStorage()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    # Регистрируем роутеры (registration должен быть первым!)
    dp.include_router(registration_router)
    dp.include_router(common_router)
    dp.include_router(messages_router)

    print("Бот запущен с системой регистрации!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())