from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TelegramUser, UserAction
from .serializers import TelegramUserSerializer, UserActionSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    permission_classes = [permissions.AllowAny]

    # Добавляем кастомный lookup_field для поиска по user_id вместо id
    lookup_field = 'user_id'
    lookup_value_regex = '[0-9]+'

    @action(detail=False, methods=['get'])
    def by_telegram_id(self, request):
        """Получить пользователя по telegram user_id"""
        user_id = request.query_params.get('user_id')
        if user_id:
            try:
                user = TelegramUser.objects.get(user_id=user_id)
                serializer = self.get_serializer(user)
                return Response(serializer.data)
            except TelegramUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
        return Response({'error': 'user_id parameter required'}, status=400)


class UserActionViewSet(viewsets.ModelViewSet):
    queryset = UserAction.objects.all()
    serializer_class = UserActionSerializer
    permission_classes = [permissions.AllowAny]