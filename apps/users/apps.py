from django.apps import AppConfig


# Конфигурация приложения 
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'users'
