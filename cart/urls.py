from django.urls import path
from .import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('clear/', views.cart_clear, name='cart_clear'),
    path('create-checkout-session/<int:item_id>/', views.create_checkout_session, name='create_checkout_session'),  # путь к оплате товара
    path('success_pay/', views.success_pay, name='success_pay'),       # путь успешной оплаты  
    path('create_all_checkout_session/<str:item_ids>/', views.create_all_checkout_session, name='create_all_checkout_session'), # путь оплаты корзины
    path('delate_order/<int:order_id>/', views.delete_order, name='delete_order'),
]
