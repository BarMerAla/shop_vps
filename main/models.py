from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Product(models.Model):
    name = models.CharField(verbose_name="Название товара", max_length=100, unique=True)
    price = models.PositiveIntegerField(verbose_name="Цена товара")
    maker = models.ForeignKey("Maker", on_delete=models.PROTECT, verbose_name="Производитель", null=True, blank=True)
    description = models.TextField(verbose_name="Описание товара", default="")
    category = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name="Категория", null=True, blank=True)
    color = models.CharField(verbose_name="Цвет товара", max_length=50, null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name="Количество товара", default=0)
    photo = models.ImageField(verbose_name="Фото товара", upload_to="photo/%Y/%m/%d", null=True, blank=True)
    full_description = RichTextField(verbose_name="Полное описание товара", default="")
    
    def __str__(self):
        return f"{self.name} - {self.price} тенге - {self.category}"
      
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["name", "maker", "category", "color"], name="unique_product")
        ]
        
class Category(models.Model):
    name = models.CharField(verbose_name="Название категории", max_length=60)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"] 
        
   
class Maker(models.Model):
    name = models.CharField(verbose_name="Название производителя", max_length=60, unique=True)
    country = models.CharField(verbose_name="Страна производителя", max_length=100)
    
    def __str__(self):
        return f"{self.name} - {self.country}"
    
    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
        ordering = ["name"]
        constraints = [                  
            models.UniqueConstraint(fields=["name", "country"], name="unique_maker")
        ]
        
        
class InStock(models.Model):
    product = models.OneToOneField("Product", on_delete=models.CASCADE, related_name="stock", verbose_name="Товар") # Связываем с Product
    quantity = models.PositiveIntegerField(verbose_name="Количество товара", default=0)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} шт."
    
    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"
        
    
    