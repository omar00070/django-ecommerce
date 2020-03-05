from django.urls import path
from .views import (HomeView, ProductDetail, 
add_to_cart, remove_from_cart, order_summery
)


app_name = 'core'

urlpatterns = [
path('', HomeView.as_view(), name='home'),
path('product/<slug>/', ProductDetail.as_view(), name='product-detail'),
path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
path('order-summery/', order_summery, name='order-summery'),
]
