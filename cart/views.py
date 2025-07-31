from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .forms import *
from .cart import *
from .models import *
from main.models import Product
from django.contrib import messages
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY   # api key Stripe

@require_POST
def cart_add(request, product_id):         # функция добавления товара/товаров в корзину
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    form = CartAddForm(request.POST)
    one_form = CartAddOneForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        if cd['cart_quantity'] == 0:
            cart.remove(product)
            messages.error(request, f"{product.name} удален из корзины")
            return redirect('cart:cart_detail')
        else:
            cart.add(product=product, cart_quantity=cd['cart_quantity'], update_quantity=cd['update'])
        messages.success(request, f"{product.name} добавлен в корзину")
    elif one_form.is_valid():
        cd = one_form.cleaned_data
        cart.add(product=product, cart_quantity=cd['cart_quantity'], update_quantity=cd['update']) 
        messages.success(request, f"{product.name} добавлен в корзину")          
    return redirect('cart:cart_detail')    
    
def cart_remove(request, product_id):   # функция удаления товара из корзины
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):         # функция отображения детали корзины
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddForm(initial={'cart_quantity': item['cart_quantity'], 'update': True})
    return render(request, 'cart/cart_detail.html', {'cart':cart,
                                                     'show_navbar': False,             # скрываем верхнее меню на этой странице
                                                     'stripe_public_key': settings.STRIPE_PUBLIC_KEY,})   

def cart_clear(request):        # функция очистки корзины
    cart = Cart(request)
    messages.success(request, "Корзина очищена!")
    cart.clear()
    return redirect('cart:cart_detail')     

# ↓ Вьюха оплаты

@login_required
def success_pay(request):
    cart = Cart(request)
    order = Order.objects.create(user=request.user, status='paid', paid=True)
    
    # 1. Если в корзине есть товары → обычная покупка
    if len(cart) > 0:
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['cart_quantity']
            )
        cart.clear()
        
    # 2. Если в сессии есть single_item → покупка одного товара    
    elif 'single_item' in request.session:
        data = request.session['single_item']
        product = Product.objects.get(id=data['product_id'])
        OrderItem.objects.create(
                order=order,
                product=product,
                price=data['price'],
                quantity=data['quantity']
                )
        del request.session['single_item']
    return render(request, 'cart/success_pay.html', {'order': order})

@csrf_exempt
def create_checkout_session(request, item_id):             # функция оплаты одного товара
    if request.method == "POST":
        item = get_object_or_404(Product, id=item_id)
        
         # Сохраняем товар в сессии
        request.session['single_item'] = {
            'product_id': item.id,
            'price': float(item.price),
            'quantity': 1
        }
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items = [{
                'price_data': {
                    'currency': 'kzt',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100), # Stripe требует цену в тыийнах
                },
                'quantity': 1,
            }],
            mode = 'payment',
            success_url='https://marketplace-audioshop.onrender.com/cart/success_pay/',
            cancel_url='https://marketplace-audioshop.onrender.com/',
        )
        return JsonResponse({'id': session.id})
    
        
@csrf_exempt
def create_all_checkout_session(request, item_ids):         # функция оплаты итоговой суммы в корзине
    if request.method == "POST":
        cart = Cart(request)
        
        # ↓ Сначала проверим сумму
        total = sum(item['product'].price * item['cart_quantity'] for item in cart)
        if total > 999999.99:
            return JsonResponse(
                {'error': 'Сумма заказа превышает лимит (999,999.99 ₸). Удалите часть товаров и попробуйте снова.'},
                status=400
            )
            
         #  Преобразуем строку item_ids в список int
        ids = [int(i) for i in item_ids.split(",") if i.strip().isdigit()]
        items = Product.objects.filter(id__in=ids)
        
        line_items = []
        for item in cart:
            line_items.append({
                'price_data': {
                    'currency': 'kzt',
                    'unit_amount': int(item['product'].price * 100),
                    'product_data': {
                        'name': item['product'].name,
                    },
                },
                'quantity': item['cart_quantity'],
            })
            
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items = line_items,
            mode = 'payment',
            success_url='https://marketplace-audioshop.onrender.com/cart/success_pay/',
            cancel_url='https://marketplace-audioshop.onrender.com/',
        )
        return JsonResponse({'id': session.id})
   
@login_required
def delete_order(request, order_id):                 # удаление отдельного заказа
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    return redirect('userauth:cab')
 