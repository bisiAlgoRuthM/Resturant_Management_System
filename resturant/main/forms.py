from django import forms
from .models import Ingredient
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'price', 'available_units']
