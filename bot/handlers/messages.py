from aiogram import Router, types
from bot.services.django_api import DjangoAPI

router = Router()
django_api = DjangoAPI()


@router.message()
async def handle_all_messages(message: types.Message):
    # Сохраняем действие "message" для аналитики
    await django_api.create_user_action(
        telegram_user_id=message.from_user.id,  # Первый аргумент
        action_type="message",  # Второй аргумент
        action_data={  # Третий аргумент
            "text": message.text[:500] if message.text else "",
            "message_id": message.message_id
        }
    )

    # Простой эхо-ответ
    if message.text:
        await message.answer(f"Вы написали: {message.text[:100]}...")