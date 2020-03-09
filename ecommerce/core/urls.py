from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (HomeView, ProductDetail, 
add_to_cart, remove_from_cart, OrderSummery,
remove_single_item_from_cart, CheckoutView,
PaymentView
)


app_name = 'core'

urlpatterns = [
path('', HomeView.as_view(), name='home'),
path('product/<slug>/', ProductDetail.as_view(), name='product-detail'),
path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-item-from-cart'),
path('order-summery/', OrderSummery.as_view(), name='order-summery'),
path('checkout/', CheckoutView.as_view(), name='checkout'),
path('payment/<payment_options>/', PaymentView.as_view(), name='payment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)