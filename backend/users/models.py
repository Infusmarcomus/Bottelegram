from django.db import models

class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True, verbose_name="ID пользователя")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Username")
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Фамилия")
    language_code = models.CharField(max_length=10, null=True, blank=True, verbose_name="Язык")
    is_bot = models.BooleanField(default=False, verbose_name="Бот")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"
        ordering = ['-created_at']

    def __str__(self):
        if self.username:
            return f"{self.first_name} (@{self.username})"
        return self.first_name

class UserAction(models.Model):
    ACTION_TYPES = [
        ('start', 'Команда /start'),
        ('help', 'Команда /help'),
        ('message', 'Сообщение'),
        ('callback', 'Callback запрос'),
    ]

    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES, verbose_name="Тип действия")
    data = models.JSONField(null=True, blank=True, verbose_name="Данные")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата действия")

    class Meta:
        verbose_name = "Действие пользователя"
        verbose_name_plural = "Действия пользователей"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.get_action_type_display()}"