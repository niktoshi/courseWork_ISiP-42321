import uuid
from decimal import Decimal
from django.db import models


# Модель Order описывает таблицу базы данных и связи с другими таблицами.
class Order(models.Model):
    # Первичный ключ
    order_id = models.BigAutoField(primary_key=True)
    order_num = models.CharField(max_length=50, unique=True, editable=False)
    # Внешний ключ связывает эту модель с записью из другой таблицы.
    user = models.ForeignKey('users.User', related_name='orders', on_delete=models.PROTECT)
    order_status = models.CharField(max_length=50, default='new')
    # DecimalField используется для денежных значений, чтобы избежать ошибок округления float.
    order_total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_delivery_address = models.CharField(max_length=255)
    order_delivery_date = models.DateTimeField(null=True, blank=True)
    
    PAYMENT_CHOICES = [
    ('card', 'Картой онлайн'),
    ('cash', 'Наличными при получении'),
    ('transfer', 'Переводом'),
]

    order_payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
    )

    # Дата создания заполняется автоматически при первой записи объекта.
    created_at = models.DateTimeField(auto_now_add=True)
    # Дата обновления автоматически меняется при каждом сохранении объекта.
    updated_at = models.DateTimeField(auto_now=True)

    # Класс Meta группирует связанную логику и настройки.
    class Meta:
        db_table = 'order'
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    # Метод __str__ возвращает понятное текстовое представление объекта в админке и отладке.
    def __str__(self):
        return self.order_num

    # Метод save выполняется при сохранении объекта и добавляет дополнительную подготовку данных.
    def save(self, *args, **kwargs):
        if not self.order_num:
            self.order_num = f'FL-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)

    @property
    # Свойство total_sum считает итоговую стоимость всех позиций.
    def total_sum(self):
        return self.order_total_sum


# Модель OrderItem описывает таблицу базы данных и связи с другими таблицами.
class OrderItem(models.Model):
    # Первичный ключ: уникальный идентификатор записи в таблице.
    order_item_id = models.BigAutoField(primary_key=True)
    # Внешний ключ связывает эту модель с записью из другой таблицы.
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Внешний ключ связывает эту модель с записью из другой таблицы.
    product = models.ForeignKey('catalog.Product', related_name='order_items', on_delete=models.PROTECT)
    # DecimalField используется для денежных значений, чтобы избежать ошибок округления float.
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_item_quantity = models.PositiveIntegerField(default=1)
    # DecimalField используется для денежных значений, чтобы избежать ошибок округления float.
    order_item_total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Класс Meta группирует связанную логику и настройки.
    class Meta:
        db_table = 'order_item'
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    # Метод __str__ возвращает понятное текстовое представление объекта в админке и отладке.
    def __str__(self):
        return f'{self.product} × {self.order_item_quantity}'

    # Метод save выполняется при сохранении объекта и добавляет дополнительную подготовку данных.
    def save(self, *args, **kwargs):
        if self.product_price and self.order_item_quantity:
            self.order_item_total_sum = Decimal(self.product_price) * self.order_item_quantity
        super().save(*args, **kwargs)
