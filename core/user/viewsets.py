from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.user.models import User
from core.user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вью для обработки списка пользователей"""
    http_method_names = ('patch', 'get', 'delete')
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)

        return obj


