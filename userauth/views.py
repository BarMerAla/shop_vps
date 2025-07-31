from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from cart.models import *
# Create your views here.

def user_register(request):                      # <- функция регистрации юзера
    if request.method == "POST":
        register_form = NewUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистированы!")
            return redirect('main:home_page')
        else:
            messages.error(request, "Ошибка при регистрации!")
    register_form = NewUserForm()
    return render(request=request, template_name='userauth/register.html', context={'register_form': register_form,
                                                                                    'show_navbar': False,})
    
def user_login(request):         # <- функция входа юзера
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)     #  <- базовая форма Django для аутентификации
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)  # <- authenticate проверяет на наличие такого юзера в бд
            if user is not None:
                login(request, user)
                messages.success(request, f"Вы вошли как {username}")
                return redirect('main:home_page')
        else:
            messages.error(request, "Неправильный username или пароль!")
    login_form = AuthenticationForm()
    return render(request=request, template_name='userauth/login.html', context={'login_form': login_form,
                                                                                 'show_navbar': False,})
    
def user_logout(request):   # <- функция выхода юзера
    logout(request)
    return redirect('main:home_page')
     
def user_cab(request):  # функция личного кабинета юзера
    if request.user.is_authenticated:
        cart = Cart(request)   # получаем корзину из сессии
        cart_items = list(cart)   # нужно привести к списку
        orders = Order.objects.filter(user=request.user).order_by('created')
        username = request.user.username
        email = request.user.email
        return render(request, 'userauth/cab.html', {'cart_items': cart_items,
                                                    'cart_total': cart.get_total_price(),
                                                    'orders': orders})
    return redirect('userauth:login')  # если не авторизован
    
@login_required         # <- доступ к редактированию возможен только для авторизованных пользователей.
def user_edit(request):   # функция для изменения данных
    user = request.user # <- получаем текущего пользователя
    if request.method == "POST":
        if 'update_username' in request.POST:
            username_form = UsernameUpdateForm(request.POST, instance=user)  # передаем текущего пользователя
            email_form = EmailUpdateForm(instance=user)   # Не заполняем email-form, чтобы избежать ошибок
            if username_form.is_valid():
                username_form.save()
                return redirect('userauth:cab')
            
        elif 'update_email' in request.POST:
            email_form = EmailUpdateForm(request.POST, instance=user)
            username_form = UsernameUpdateForm(instance=user)  # Не трогаем username-form
            if email_form.is_valid():
                email_form.save()
                return redirect('userauth:cab')
            
    else:
        username_form = UsernameUpdateForm()  # Загружаем текущие данные
        email_form = EmailUpdateForm()  # Загружаем текущие данные
    return render(request=request, template_name='userauth/edit.html', context={'username_form': username_form,
                                                                                'email_form': email_form})
            
@login_required
def change_pass(request):    # функция для изменения пароля
    if request.method == "POST":
        pass_form = PasswordChangeForm(user=request.user, data=request.POST)
        if pass_form.is_valid():
            user = pass_form.save()  # Сохраняем новый пароль
            update_session_auth_hash(request, user)
            messages.success(request, "Пароль успешно изменён!")
    else:
        pass_form =  PasswordChangeForm(user=request.user)
        messages.error(request, "Повторите попытку")
    return render(request=request, template_name='userauth/change_pass.html', context={'pass_form': pass_form})
        
        
     
 
                

                
            
            
    