from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.cart.utils import get_or_create_cart
from .forms import CheckoutForm
from .models import Order, OrderItem


@login_required
# Представление checkout оформляет заказ из текущей корзины.
def checkout(request):
    cart = get_or_create_cart(request.user)
    items = cart.items.select_related('product').all()
    if not items.exists():
        messages.warning(request, 'Корзина пуста. Добавьте товары перед оформлением заказа.')
        return redirect('catalog:catalog')

    initial = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone,
        'email': request.user.email,
        'address': request.user.address,
    }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.phone = form.cleaned_data['phone']
            request.user.email = form.cleaned_data['email']
            request.user.address = f"{form.cleaned_data['city']}, {form.cleaned_data['address']}"
            request.user.save()

            order = Order.objects.create(
                user=request.user,
                order_delivery_address=request.user.address,
                order_delivery_date=form.cleaned_data.get('delivery_date'),
                order_payment_method=form.cleaned_data['payment_method'],
                order_total_sum=cart.total_sum,
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_price=item.product.product_new_price,
                    order_item_quantity=item.quantity,
                    order_item_total_sum=item.line_total,
                )
            items.delete()
            messages.success(request, f'Заказ {order.order_num} успешно оформлен.')
            return redirect('orders:detail', order_id=order.order_id)
    else:
        form = CheckoutForm(initial=initial)

    return render(request, 'checkout.html', {'form': form, 'cart': cart, 'items': items})


@login_required
# показать пользователю список его заказов.
def orders_list(request):
    orders = request.user.orders.prefetch_related('items__product').all()
    return render(request, 'orders/list.html', {'orders': orders})


@login_required
# Представление order_detail показывает детали конкретного заказа пользователя.
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), pk=order_id, user=request.user)
    return render(request, 'order-detail.html', {'order': order})
