from django.apps import AppConfig


# Конфигурация приложения OrdersConfig: Django использует её при подключении приложения.
class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.orders'
    verbose_name = 'orders'
