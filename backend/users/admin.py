from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import TelegramUser, UserAction


def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="telegram_users.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'User ID', 'Username', 'First Name', 'Last Name', 'Registration Date'])

    for obj in queryset:
        writer.writerow([
            obj.id,
            obj.user_id,
            obj.username or '',
            obj.first_name,
            obj.last_name or '',
            obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response


export_to_csv.short_description = "Экспорт выбранных пользователей в CSV"


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'first_name', 'last_name', 'created_at', 'actions_count']
    list_filter = ['created_at', 'language_code']
    search_fields = ['user_id', 'username', 'first_name', 'last_name']
    readonly_fields = ['created_at', 'updated_at']
    actions = [export_to_csv]

    def actions_count(self, obj):
        return obj.useraction_set.count()

    actions_count.short_description = 'Кол-во действий'


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_type', 'created_at', 'short_data']
    list_filter = ['action_type', 'created_at']
    readonly_fields = ['created_at']
    search_fields = ['user__user_id', 'user__username', 'user__first_name']

    def short_data(self, obj):
        return str(obj.data)[:50] + '...' if obj.data else '-'

    short_data.short_description = 'Данные'

# УДАЛИ ЭТИ СТРОКИ ЕСЛИ ОНИ ЕСТЬ (они создают двойную регистрацию):
# admin.site.register(TelegramUser, TelegramUserAdmin)
# admin.site.register(UserAction, UserActionAdmin)