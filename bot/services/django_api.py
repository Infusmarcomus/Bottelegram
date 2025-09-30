import aiohttp
import asyncio
import json


class DjangoAPI:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url

    async def create_user(self, user_data: dict):
        """Создает пользователя в Django через API"""
        url = f"{self.base_url}/users/"

        print(f"📡 Отправка запроса к: {url}")
        print(f"📦 Данные пользователя: {user_data}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=user_data) as response:
                    print(f"📊 Статус ответа: {response.status}")

                    response_text = await response.text()
                    print(f"📄 Тело ответа: {response_text}")

                    if response.status == 201:
                        print("✅ Пользователь успешно создан!")
                        return await response.json()
                    else:
                        print(f"❌ Ошибка создания пользователя: {response.status}")
                        return None
        except Exception as e:
            print(f"💥 Исключение при запросе: {e}")
            return None

    async def get_user_by_telegram_id(self, telegram_user_id: int):
        """Получает пользователя по telegram user_id"""
        url = f"{self.base_url}/users/by_telegram_id/?user_id={telegram_user_id}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        user_data = await response.json()
                        print(f"✅ Найден пользователь: ID={user_data['id']}, user_id={user_data['user_id']}")
                        return user_data
                    else:
                        print(f"❌ Пользователь {telegram_user_id} не найден")
                        return None
        except Exception as e:
            print(f"💥 Ошибка поиска пользователя: {e}")
            return None

    async def create_user_action(self, telegram_user_id: int, action_type: str, action_data: dict = None):
        """Создает действие пользователя"""
        # Сначала получаем пользователя из базы
        user = await self.get_user_by_telegram_id(telegram_user_id)

        if not user:
            print(f"❌ Не могу создать действие - пользователь {telegram_user_id} не найден")
            return None

        url = f"{self.base_url}/actions/"

        # ИСПРАВЛЕНО: используем 'id' из базы данных для ForeignKey
        corrected_data = {
            "user": user["id"],  # ← ВАЖНО: это ID записи в таблице TelegramUser (3), а не user_id
            "action_type": action_type,
            "data": action_data or {}
        }

        print(f"📡 Отправка действия к: {url}")
        print(f"📦 Данные действия: {corrected_data}")
        print(f"🔍 Используем ID пользователя из базы: {user['id']} (telegram user_id: {user['user_id']})")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=corrected_data) as response:
                    response_text = await response.text()
                    print(f"📊 Статус ответа действия: {response.status}")
                    print(f"📄 Тело ответа действия: {response_text}")

                    if response.status == 201:
                        print("✅ Действие успешно создано!")
                        return await response.json()
                    else:
                        print(f"❌ Ошибка создания действия: {response.status}")
                        try:
                            error_data = json.loads(response_text)
                            print(f"🔍 Детали ошибки: {error_data}")
                        except:
                            pass
                        return None
        except Exception as e:
            print(f"💥 Ошибка действия: {e}")
            return None