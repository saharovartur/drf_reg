from rest_framework import serializers
from core.user.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор списка юзеров."""
    id = serializers.UUIDField(source='public_id',
                                read_only=True,
                               format='hex')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created',
                  'first_name', 'last_name', 'updated']
        read_only_field = ['is_active']
