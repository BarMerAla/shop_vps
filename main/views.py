from django.shortcuts import get_object_or_404, render
from .models import *
from .forms import *
from django.core.paginator import Paginator
from cart.forms import *
from django.db.models.functions import Lower
import stripe
from django.conf import settings


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY     # api key Stripe

def all_products(request):             # вьюха главной страницы
    items = Product.objects.all()
    brand_form = BrandFilterForm(request.GET)        # Форма для фильтрации (GET-параметры)
    selected_brands = request.GET.getlist("brand")
    cart_one_form = CartAddOneForm()
    price_range = request.GET.get("price_range")
    category_id = request.GET.get("category")
    color = request.GET.get("color")
    country = request.GET.get("country")
    search_all = request.GET.get("search_all")
    categories = Category.objects.all()
    makers = Maker.objects.all()
     
    if brand_form.is_valid() and brand_form.cleaned_data['brand']:           # фильтрация по брендам
        items = items.filter(maker__in=brand_form.cleaned_data['brand'])
        
    if price_range == "1":                          # фильтрация по ценам
        items = items.filter(price__lte=300000)
        
    if price_range == "2":
        items = items.filter(price__gte=300001, price__lte=600000)
        
    if price_range == "3":
        items = items.filter(price__gte=600001)
    
    if category_id:                                   # фильтрация по категориям
        items = items.filter(category_id=category_id)
        
    if color:                                        # фильтрация по цветам
        items = items.filter(color=color)
        
    if country:                                     # фильтрация по странам
        maker = makers.filter(country=country)
        items = items.filter(maker__in=maker)
        
    if search_all:                          # поиск в каталоге по названию
        items = items.filter(name__icontains=search_all)
        
    raw_colors = (Product.objects.exclude(color__isnull=True)   #  Получаем цвета, приводим к нижнему регистру, фильтруем, чистим
                  .exclude(color__exact='')
                  .values_list('color', flat=True))
    
    colors = sorted(set(color.strip() for color in raw_colors))  # Убираем дубликаты с учётом регистра и лишних пробелов
    
    raw_countries = (Maker.objects.exclude(country__exact='')
                    .values_list('country', flat=True))
    
    countries = sorted(set(country.strip() for country in raw_countries))
    
    paginator = Paginator(items, 20)  # 20 товаров на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/home_page.html', {'items': page_obj,
                                                   'brand_form': brand_form, 
                                                   'selected_brands': selected_brands,
                                                   'cart_one_form': cart_one_form,
                                                   'page_obj': page_obj,
                                                   'color': color,
                                                   'category_id': category_id,
                                                   'country': country,
                                                   'countries': countries,
                                                   'categories': categories,
                                                   'colors': colors,
                                                   'search-all': search_all,
                                                   'show_navbar': True, })
                                                

def product_detail(request, item_id):         # вьюха деталей продуктов
    item = Product.objects.get(id = item_id)
    cart_one_form = CartAddOneForm()
     
    return render(request, 'main/product_detail.html', {'item': item,
                                                        'cart_one_form': cart_one_form,
                                                        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                                                        'show_navbar': False,})

def contact_view(request):
    return render(request, 'main/contacts.html')
    
