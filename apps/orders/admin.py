from django.contrib import admin
from .models import Order, OrderItem


# Inline-класс OrderItemInline показывает связанные записи прямо внутри страницы родительской модели в админке.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('order_item_total_sum',)


@admin.register(Order)
# Админ-класс OrderAdmin настраивает, как модель отображается и редактируется в панели Django admin.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_num', 'user', 'order_status', 'order_total_sum', 'created_at')
    list_filter = ('order_status', 'created_at')
    search_fields = ('order_num', 'user__email', 'user__username')
    inlines = [OrderItemInline]
