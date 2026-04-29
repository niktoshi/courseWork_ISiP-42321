from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, ProductCategory
from django.db.models.functions import Random

INSPIRATION = [
    {'title': 'Светлая гостиная', 'image': '/static/images/inspire1.png'},
    {'title': 'Кухня в пастельных оттенках', 'image': '/static/images/inspire2.png'},
    {'title': 'Ванная в тёплых тонах', 'image': '/static/images/inspire3.png'},
]
SERVICES = [
    {'title': 'Доставка от 1 дня', 'button': 'Выбрать город', 'style': 'sage'},
    {'title': 'Самовывоз', 'button': 'Подробнее', 'style': 'sage'},
    {'title': 'Планирование кухни', 'button': 'Связаться', 'style': 'blush'},
]



def home(request):
    featured_products = Product.objects.order_by(Random())[:6]
    return render(request, 'index.html', {
        'featured_products': featured_products,
        'inspiration': INSPIRATION,
        'services': SERVICES,
        'categories_for_mosaic': ProductCategory.objects.all()[:6],
    })



def catalog_list(request):
    category_slug = request.GET.get('category', '').strip()
    query = request.GET.get('q', '').strip()
    products = Product.objects.select_related('product_category').all()
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(ProductCategory, product_category_slug=category_slug)
        products = products.filter(product_category=selected_category)
    if query:
        products = products.filter(
            Q(product_name__icontains=query)
            | Q(product_description__icontains=query)
            | Q(product_material__icontains=query)
            | Q(product_color__icontains=query)
        )

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'catalog.html', {
        'products': page_obj,
        'page_obj': page_obj,
        'selected_category': selected_category,
        'current_category': category_slug,
        'query': query,
        'all_categories': ProductCategory.objects.all(),
    })


# Представление product_detail показывает подробную страницу товара.
def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('product_category').prefetch_related('gallery'),
        product_slug=slug,
    )
    related_products = Product.objects.filter(product_category=product.product_category).exclude(pk=product.pk)[:3]
    return render(request, 'product.html', {
        'product': product,
        'related_products': related_products,
    })


# Представление about отдаёт информационную страницу о магазине.
def about(request):
    return render(request, 'about.html')


# Представление contacts отдаёт страницу с контактной информацией.
def contacts(request):
    if request.method == 'POST':
        messages.success(request, 'Сообщение отправлено. Мы свяжемся с вами.')
        return redirect('catalog:contacts')
    return render(request, 'contacts.html')
