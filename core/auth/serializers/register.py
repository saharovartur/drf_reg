from rest_framework import serializers

from core.user.models import User
from core.user.serializers import UserSerializer


class RegisterSerializer(UserSerializer):
    """Сериализатор регистрации для
    запросов и создания пользователей"""
    password = serializers.CharField(write_only=True,
                                     max_length=128,
                                     min_length=8,
                                     required=True)

    class Meta:
        model = User
        # # Список всех полей, которые могут быть включены в запрос или ответ
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        #Вызов метода create
        return User.objects.create_user(**validated_data)




