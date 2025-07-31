from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):    # <- форма создания юзера
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "form-input"}))
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={"class": "form-input"}))
    password1 = forms.CharField(required=True, label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"}))
    password2 = forms.CharField(required=True, label="Повторите пароль", widget=forms.PasswordInput(attrs={"class": "form-input"}))
    
    class Meta:
        model = User   # <- модель наследуется от базового класса User от Django
        fields = ["username", "email", "password1", "password2"]
        
    def save(self, commit=True): # <- функция сохраняет пользователя в бд
        user = super(NewUserForm, self).save(commit=False)
        # ↑ False позволяет сначала модифицировать объект, а затем сохранить его, избегая промежуточного сохранения в базу
        user.email = self.cleaned_data.get("email")  # Используем get(), чтобы избежать ошибки KeyError, если email по какой-то причине отсутствует
        if commit:
            user.save()
        return user
        
class UsernameUpdateForm(forms.ModelForm):    # <- форма изменения username
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "forms-input"}))
    
    class Meta:
        model = User
        fields = ["username"]
        
class EmailUpdateForm(forms.ModelForm):     # <- форма изменения почты
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={"class": "forms-input"}))
        
    class Meta:
        model = User
        fields = ["email"]
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        # ↓ выполняет проверку уникальности email, исключая текущего пользователя
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("Этот email уже испольузется!")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
            