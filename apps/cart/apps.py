from django.apps import AppConfig


# Конфигурация приложения CartConfig: Django использует её при подключении приложения.
class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cart'
    verbose_name = 'cart'
