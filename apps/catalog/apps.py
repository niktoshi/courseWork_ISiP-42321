from django.apps import AppConfig


# Конфигурация приложения 
class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.catalog'
    verbose_name = 'catalog'
