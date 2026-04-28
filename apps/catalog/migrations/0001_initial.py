import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('product_category_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('product_category_name', models.CharField(max_length=255)),
                ('product_category_slug', models.SlugField(max_length=255, unique=True)),
                ('product_category_description', models.TextField(blank=True)),
                ('product_category_image', models.ImageField(blank=True, null=True, upload_to='categories/')),
                ('product_category_order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_category_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='catalog.productcategory')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'product_category',
                'ordering': ['product_category_order', 'product_category_name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('product_slug', models.SlugField(max_length=255, unique=True)),
                ('product_description', models.TextField(blank=True)),
                ('product_new_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('product_old_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('product_material', models.CharField(blank=True, max_length=100)),
                ('product_color', models.CharField(blank=True, max_length=100)),
                ('product_width', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('product_height', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('product_in_stock', models.BooleanField(default=True)),
                ('product_stock_quantity', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='catalog.productcategory')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'products',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('product_image_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('product_image', models.ImageField(upload_to='products/gallery/')),
                ('product_alt', models.CharField(blank=True, max_length=255)),
                ('product_order', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='catalog.product')),
            ],
            options={
                'verbose_name': 'Изображение товара',
                'verbose_name_plural': 'Изображения товаров',
                'db_table': 'product_image',
                'ordering': ['product_order', 'product_image_id'],
            },
        )
    ]
