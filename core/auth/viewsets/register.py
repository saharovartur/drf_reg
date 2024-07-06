from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from core.auth.serializers.register import RegisterSerializer


class RegisterViewSet(ViewSet):
    """Регистрация"""
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        confirmation_link = f"http://example.com/confirm/{user.id}/"

        # Отправка письма с подтверждением
        send_mail(
            'Подтвердите свой аккаунт',
            'Спасибо за регистрацию! '
            'Пожалуйста, подтвердите свой аккаунт, перейдя по следующей ссылке:' f'{confirmation_link}',
            'noreply@yourapp.com',
            [user.email],
            fail_silently=False,
        )

        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response ({'user': serializer.data,
                          'refresh': res['refresh'],
                          'token': res['access']
                          }, status=status.HTTP_201_CREATED)

