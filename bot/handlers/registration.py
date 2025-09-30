from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from bot.states.user_registration import RegistrationStates
from bot.services.django_api import DjangoAPI
import re

router = Router()
django_api = DjangoAPI()

# Список нецензурных слов для проверки (можно расширить)
BAD_WORDS = [
    # Основные матерные слова
    'хуй','пидорас', 'пидор', 'хуё', 'хуя', 'хую', 'хуе',
    'пизд', 'пизд',
    'ебан', 'ебать', 'ебли', 'ебал', 'ебаш', 'ебис',
    'ёбан', 'ёбать', 'ёбли', 'ёбал', 'ёбаш', 'ёбис',
    'мудак', 'мудил', 'мудозвон',
    'гандон', 'гондон',
    'блядь', 'бляд', 'бля',
    'сука', 'суки', 'сучк',
    'гондон',
    'шлюха', 'шлюх',
    'проститутка', 'проститутк',
    'педик', 'пидор', 'пидорас', 'пидарас', 'пидр',
    'гомик',

    # Оскорбительные производные
    'охуен', 'охуит', 'охуе',
    'похуй', 'похую',
    'разъеб', 'разъёб',
    'уебан', 'уёбан',
    'заеб', 'заёб',
    'съеб', 'съёб',
    'выеб', 'выебан',

    # Менее грубые, но все равно оскорбительные
    'долбоёб', 'долбоеб',
    'конча', 'конч',
    'мразь', 'мрази',
    'ублюдок', 'ублюдк',
    'выблядок', 'выблядк',
    'сволоч', 'сволочь',
    'тварь', 'твари',
    'падла', 'падл',
    'гнил', 'гнид',
    'черт', 'чёрт', 'чорт',

    # Английские маты (на всякий случай)
    'fuck', 'fucking', 'fucker',
    'shit', 'shitting', 'bullshit',
    'asshole', 'dick', 'cock', 'pussy', 'cunt',
    'bitch', 'bastard', 'whore', 'slut',
    'damn', 'god damn',
    'motherfucker', 'motherfucking',

    # Оскорбления по национальности/признакам
    'жид', 'жидов',
    'чурк', 'хач', 'черножоп', 'узкоглаз',
    'даун', 'дебил', 'идиот', 'кретин', 'умственноотстал',

    # Другие оскорбления
    'дегенерат', 'дебил', 'идиот', 'дурак', 'олень', 'козел',
    'придурок', 'тупиц', 'олух', 'болван',
]

def contains_bad_words(text: str) -> bool:
    """Проверяет текст на наличие нецензурных слов"""
    text_lower = text.lower()
    return any(bad_word in text_lower for bad_word in BAD_WORDS)


def is_valid_name(name: str) -> bool:
    """Проверяет корректность имени"""
    # Имя должно содержать только буквы и быть от 2 до 50 символов
    if len(name) < 2 or len(name) > 50:
        return False

    # Проверяем на наличие только букв и некоторых специальных символов
    if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$', name):
        return False

    # Проверяем на мат
    if contains_bad_words(name):
        return False

    return True


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    # Сохраняем пользователя в Django
    user_data = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "language_code": message.from_user.language_code,
        "is_bot": False
    }

    await django_api.create_user(user_data)

    # Начинаем процесс регистрации
    keyboard = [
        [types.KeyboardButton(text="🇷🇺 Русский")],
        [types.KeyboardButton(text="🇺🇸 English")]
    ]
    reply_markup = types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "👋 Добро пожаловать! / Welcome!\n\n"
        "🌍 Выберите язык / Choose language:",
        reply_markup=reply_markup
    )

    await state.set_state(RegistrationStates.choosing_language)


@router.message(RegistrationStates.choosing_language, F.text.in_(["🇷🇺 Русский", "🇺🇸 English"]))
async def language_chosen(message: types.Message, state: FSMContext):
    language = "ru" if message.text == "🇷🇺 Русский" else "en"

    # Сохраняем выбранный язык в состоянии
    await state.update_data(language=language)

    # Убираем клавиатуру
    remove_keyboard = types.ReplyKeyboardRemove()

    if language == "ru":
        text = "Отлично! Давайте познакомимся 😊\n\nКак вас зовут?"
    else:
        text = "Great! Let's get acquainted 😊\n\nWhat's your name?"

    await message.answer(text, reply_markup=remove_keyboard)
    await state.set_state(RegistrationStates.entering_name)


@router.message(RegistrationStates.choosing_language)
async def wrong_language_choice(message: types.Message):
    """Обработка неправильного выбора языка"""
    await message.answer(
        "❌ Пожалуйста, выберите язык из предложенных вариантов.\n"
        "❌ Please choose a language from the options provided."
    )


@router.message(RegistrationStates.entering_name)
async def name_entered(message: types.Message, state: FSMContext):
    name = message.text.strip()
    user_data = await state.get_data()
    language = user_data.get('language', 'ru')

    # Проверяем имя
    if not is_valid_name(name):
        if language == "ru":
            await message.answer(
                "❌ Это имя некорректное. Пожалуйста, введите настоящее имя:\n"
                "• Только буквы\n"
                "• От 2 до 50 символов\n"
                "• Без нецензурных слов"
            )
        else:
            await message.answer(
                "❌ This name is invalid. Please enter a real name:\n"
                "• Letters only\n"
                "• 2-50 characters\n"
                "• No offensive words"
            )
        return

    # Сохраняем имя в состоянии
    await state.update_data(user_name=name)

    # Сохраняем действие в Django
    await django_api.create_user_action(
        telegram_user_id=message.from_user.id,
        action_type="registration_complete",
        action_data={"name": name, "language": language}
    )

    # Завершаем регистрацию
    if language == "ru":
        text = f"""
✅ Отлично, {name}! Приятно познакомиться!

Регистрация завершена! Теперь вы можете пользоваться ботом.

Доступные команды:
/help - Помощь
/profile - Ваш профиль
        """
    else:
        text = f"""
✅ Great, {name}! Nice to meet you!

Registration completed! You can now use the bot.

Available commands:
/help - Help
/profile - Your profile
        """

    await message.answer(text)
    await state.clear()


@router.message(RegistrationStates.entering_name)
async def invalid_name(message: types.Message, state: FSMContext):
    """Обработка неправильного имени (запасной хендлер)"""
    user_data = await state.get_data()
    language = user_data.get('language', 'ru')

    if language == "ru":
        await message.answer("❌ Пожалуйста, введите корректное имя.")
    else:
        await message.answer("❌ Please enter a valid name.")