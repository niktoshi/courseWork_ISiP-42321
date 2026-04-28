from apps.catalog.models import ProductCategory
from apps.cart.models import Cart


# Контекст-процессор добавляет общие данные во все шаблоны сайта.
def global_context(request):
    categories = ProductCategory.objects.all()[:8]
    cart_count = 0
    if getattr(request, 'user', None) and request.user.is_authenticated:
        try:
            cart_count = request.user.cart.total_items
        except Cart.DoesNotExist:
            cart_count = 0
    return {
        'site_categories': categories,
        'cart_count': cart_count,
    }
