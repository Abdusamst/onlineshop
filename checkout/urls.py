from django.urls import path

from .views import checkout, create_order_whatsapp, thank_you

app_name = 'checkout'

urlpatterns = [
    path('', checkout, name='checkout'),
    path('create_order_whatsapp/', create_order_whatsapp, name='create_order_whatsapp'),
    path('thank-you/<int:order_id>/', thank_you, name='thank_you'),
]
