from aiogram import Router, types
from aiogram.filters import Command
from bot.services.django_api import DjangoAPI

router = Router()
django_api = DjangoAPI()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
🤖 Доступные команды:

/start - Начать работу
/help - Помощь
/profile - Информация о профиле
/stats - Статистика

Админка: http://localhost:8000/admin/
"""
    await message.answer(help_text)

@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    profile_text = f"""
📊 Ваш профиль:

ID: {message.from_user.id}
Имя: {message.from_user.first_name}
Фамилия: {message.from_user.last_name or 'Не указана'}
Username: @{message.from_user.username or 'Не указан'}
Язык: {message.from_user.language_code}
"""
    await message.answer(profile_text)