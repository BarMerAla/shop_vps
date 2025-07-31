from django.urls import path
from .import views

app_name = 'main'

urlpatterns = [
    path('', views.all_products, name='home_page'),
    path('<int:item_id>/', views.product_detail, name='product_detail'),
    path('contacts/', views.contact_view, name='contacts'),
]
