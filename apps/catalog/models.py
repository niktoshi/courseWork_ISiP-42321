from django.db import models
from django.urls import reverse


# Модель ProductCategory описывает таблицу базы данных и связи с другими таблицами.
class ProductCategory(models.Model):
    product_category_id = models.BigAutoField(primary_key=True)
    product_category_name = models.CharField(max_length=255)
    # SlugField хранит короткий URL-фрагмент для красивых адресов страниц.
    product_category_slug = models.SlugField(max_length=255, unique=True)
    product_category_description = models.TextField(blank=True)
    product_category_image = models.ImageField(upload_to='categories/', blank=True, null=True)
    # Внешний ключ связывает эту модель с записью из другой таблицы.
    product_category_parent = models.ForeignKey(
        'self', related_name='children', on_delete=models.SET_NULL, null=True, blank=True
    )
    product_category_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Класс Meta группирует связанную логику и настройки.
    class Meta:
        db_table = 'product_category'
        ordering = ['product_category_order', 'product_category_name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    # Метод __str__ возвращает понятное текстовое представление объекта в админке и отладке.
    def __str__(self):
        return self.product_category_name

    @property
    def name(self):
        return self.product_category_name

    @property
    def slug(self):
        return self.product_category_slug

    @property
    def description(self):
        return self.product_category_description


# Модель Product описывает таблицу базы данных и связи с другими таблицами.
class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    # SlugField хранит короткий URL-фрагмент для красивых адресов страниц.
    product_slug = models.SlugField(max_length=255, unique=True)
    product_category = models.ForeignKey(ProductCategory, related_name='products', on_delete=models.PROTECT)
    product_description = models.TextField(blank=True)
    product_new_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product_old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Поле изображения хранит путь к загруженному файлу картинки.
    product_image = models.ImageField(upload_to='products/', blank=True, null=True)
    product_material = models.CharField(max_length=100, blank=True)
    product_color = models.CharField(max_length=100, blank=True)
    product_width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_in_stock = models.BooleanField(default=True)
    product_stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Класс Meta группирует связанную логику и настройки.
    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    # Метод __str__ возвращает понятное текстовое представление объекта в админке и отладке.
    def __str__(self):
        return self.product_name

    # Метод get_absolute_url возвращает основной адрес страницы этого объекта.
    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.product_slug})

    @property

    def name(self):
        return self.product_name

    @property

    def slug(self):
        return self.product_slug
    @property

    def description(self):
        return self.product_description

    @property

    def price(self):
        return self.product_new_price

    @property
    def old_price(self):
        return self.product_old_price

    @property
    def image_url(self):
        if self.product_image:
            return self.product_image.url

        first = self.gallery.first()
        if first:
            return first.product_image.url

        return '/static/images/no-image.png'

    @property
    def material(self):
        return self.product_material

    @property
    def color(self):
        return self.product_color

    @property
    def category_name(self):
        return self.product_category.product_category_name


# Модель ProductImage описывает таблицу базы данных и связи с другими таблицами.
class ProductImage(models.Model):
    product_image_id = models.BigAutoField(primary_key=True)
    # Внешний ключ связывает эту модель с записью из другой таблицы.
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    # Поле изображения хранит путь к загруженному файлу картинки.
    product_image = models.ImageField(upload_to='products/gallery/')
    product_alt = models.CharField(max_length=255, blank=True)
    product_order = models.IntegerField(default=0)

    # Класс Meta группирует связанную логику и настройки.
    class Meta:
        db_table = 'product_image'
        ordering = ['product_order', 'product_image_id']
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    # Метод __str__ возвращает понятное текстовое представление объекта в админке и отладке.
    def __str__(self):
        return f'{self.product} #{self.product_image_id}'
