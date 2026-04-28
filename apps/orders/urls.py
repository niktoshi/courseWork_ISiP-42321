from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.orders_list, name='list'),
    path('checkout/', views.checkout, name='checkout'),
    path('detail/<int:order_id>/', views.order_detail, name='detail'),
]
