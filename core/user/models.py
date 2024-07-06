import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404


class UserManager(BaseUserManager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise Http404("User not found")

    def create_user(self, email, username, password=None, **kwargs):
        """Создадим и вернем юзера с данными"""
        if username is None:
            raise TypeError('Укажите имя')
        if email is None:
            raise TypeError('Укажите email')
        if password is None:
            raise TypeError('Укажите пароль')

        user = self.model(username=username,
                          email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password, **kwargs):
        """Создадим и вернем суперпользователя с данными"""
        if password is None:
            raise TypeError('Укажите пароль')
        if email is None:
            raise TypeError('Укажите email')
        if username is None:
            raise TypeError('Укажите имя')

        user = self.create_user(email, username, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(db_index=True, unique=True,
                                 default=uuid.uuid4, editable=False)
    username = models.CharField(db_index=True, max_length=30, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"