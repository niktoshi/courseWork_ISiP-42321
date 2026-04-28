from django.contrib import admin
from .models import User


@admin.register(User)
# Админ-класс UserAdmin настраивает, как модель отображается и редактируется в панели Django admin.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_superuser', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_superuser', 'created_at')
