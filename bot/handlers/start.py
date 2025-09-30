from aiogram import Router, types
from aiogram.filters import Command
from bot.services.django_api import DjangoAPI

router = Router()
django_api = DjangoAPI()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Подготавливаем данные пользователя
    user_data = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "language_code": message.from_user.language_code,
        "is_bot": False
    }

    # Сохраняем в Django
    result = await django_api.create_user(user_data)

    if result:
        # Сохраняем действие с правильными аргументами
        await django_api.create_user_action(
            telegram_user_id=message.from_user.id,  # Первый аргумент
            action_type="start",  # Второй аргумент
            action_data={  # Третий аргумент
                "command": "/start",
                "message_id": message.message_id
            }
        )

        await message.answer(
            "✅ Привет! Я бот интегрированный с Django админкой.\n"
            "Твои данные сохранены в базе!\n"
            f"Твой ID: {message.from_user.id}"
        )
    else:
        await message.answer(
            "❌ Привет! Возникла ошибка при сохранении данных.\n"
            "Но бот работает!"
        )