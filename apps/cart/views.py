from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.catalog.models import Product
from .models import CartItem
from .utils import get_or_create_cart


@login_required
# Представление cart_detail показывает страницу корзины текущего пользователя.
def cart_detail(request):
    cart = get_or_create_cart(request.user)
    items = cart.items.select_related('product').all()
    return render(request, 'cart.html', {'cart': cart, 'items': items})


@login_required
# Представление add_to_cart добавляет выбранный товар в корзину.
def add_to_cart(request, product_id):
    if request.method != 'POST':
        return redirect('catalog:product_detail', slug=get_object_or_404(Product, pk=product_id).product_slug)
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
    if not created:
        item.quantity += 1
        item.save(update_fields=['quantity'])
    messages.success(request, f'Товар «{product.product_name}» добавлен в корзину.')
    return redirect(request.POST.get('next') or 'cart:detail')


@login_required
# Представление update_cart_item увеличивает или уменьшает количество товара в корзине.
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'plus':
            item.quantity += 1
            item.save(update_fields=['quantity'])
        elif action == 'minus':
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
            else:
                item.save(update_fields=['quantity'])
    return redirect('cart:detail')


@login_required
# Представление remove_cart_item удаляет одну позицию из корзины.
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.info(request, 'Товар удалён из корзины.')
    return redirect('cart:detail')


@login_required
# Представление clear_cart полностью очищает корзину пользователя.
def clear_cart(request):
    if request.method == 'POST':
        cart = get_or_create_cart(request.user)
        cart.items.all().delete()
        messages.info(request, 'Корзина очищена.')
    return redirect('cart:detail')
