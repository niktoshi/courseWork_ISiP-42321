from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


# Класс UserManager группирует связанную логику и настройки.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, username, password, **extra_fields)


# Модель User описывает таблицу базы данных и связи с другими таблицами.
class User(AbstractBaseUser):
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    # Класс Meta группирует связанную логику и настройки.
    class Meta:
        db_table = 'user'
        ordering = ['-created_at']

    # Метод __str__ возвращает понятное текстовое представление объекта в админке и отладке.
    def __str__(self):
        return self.username or self.email

    @property
    # Функция is_staff показывает, может ли пользователь заходить в админ-панель Django.
    def is_staff(self):
        return self.is_superuser

    @property
    # Функция is_active показывает, активен ли аккаунт пользователя
    def is_active(self):
        return True

    # Функция has_perm проверяет, есть ли у пользователя конкретное разрешение
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    # Функция has_module_perms есть ли у пользователя доступ к целому приложению в админке
    def has_module_perms(self, app_label):
        return self.is_superuser
