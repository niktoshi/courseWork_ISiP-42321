from decimal import Decimal
from django.db import models


# Модель Cart описывает таблицу базы данных и связи с другими таблицами.
class Cart(models.Model):
    # Первичный ключ: уникальный идентификатор записи в таблице.
    cart_id = models.BigAutoField(primary_key=True)
    # Связь один-к-одному: у пользователя может быть только одна такая связанная запись.
    user = models.OneToOneField('users.User', related_name='cart', on_delete=models.CASCADE)
    # Дата создания заполняется автоматически при первой записи объекта.
    created_at = models.DateTimeField(auto_now_add=True)
    # Дата обновления автоматически меняется при каждом сохранении объекта.
    updated_at = models.DateTimeField(auto_now=True)

    # Класс Meta группирует связанную логику и настройки.
    class Meta:
        db_table = 'cart'
        ordering = ['-updated_at']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    # Метод __str__ возвращает понятное текстовое представление объекта в админке и отладке.
    def __str__(self):
        return f'Корзина {self.user}'

    @property
    # Свойство total_items считает общее количество товаров в корзине.
    def total_items(self):
        return sum(item.quantity for item in self.items.select_related('product'))

    @property
    # Свойство total_sum считает итоговую стоимость всех позиций.
    def total_sum(self):
        return sum((item.line_total for item in self.items.select_related('product')), Decimal('0.00'))


# Модель CartItem описывает таблицу базы данных и связи с другими таблицами.
class CartItem(models.Model):
    # Первичный ключ: уникальный идентификатор записи в таблице.
    cart_item_id = models.BigAutoField(primary_key=True)
    # Внешний ключ связывает эту модель с записью из другой таблицы.
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    # Внешний ключ связывает эту модель с записью из другой таблицы.
    product = models.ForeignKey('catalog.Product', related_name='cart_items', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    # Класс Meta группирует связанную логику и настройки.
    class Meta:
        db_table = 'cart_item'
        unique_together = ('cart', 'product')
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    # Метод __str__ возвращает понятное текстовое представление объекта в админке и отладке.
    def __str__(self):
        return f'{self.product} × {self.quantity}'

    @property
    # Свойство line_total считает сумму одной позиции: цена товара × количество.
    def line_total(self):
        return self.product.product_new_price * self.quantity
