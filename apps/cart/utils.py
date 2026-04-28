from .models import Cart


# Вспомогательная функция получает существующую корзину пользователя или создаёт новую.
def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart
