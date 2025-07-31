from django.db import models
from django.contrib.auth.models import User
from main.models import Product

# Create your models here.

class Order(models.Model):       # модель заказа (покупки)
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('failed', 'Ошибка оплаты'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)           # дата создания заказа
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')     # статус заказа
    paid = models.BooleanField(default=False)                # статус оплаты
    
    def __str__(self):
        return f"Заказ № {self.id} от {self.user.username}"
    
    def get_total_cost(self):                                          # общая сумма покупки
        return sum(item.get_cost() for item in self.items.all())
    
    
class OrderItem(models.Model):     # модель позиции (товаров) одного заказа
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_cost(self):
        return self.price * self.quantity
    
    
    
    
    