from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views import View #import generic view clas
from .models import RecipeRequirement, MenuItem, Ingredient
from .forms import IngredientForm, RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if not username:
                # Handle empty username case
                return HttpResponse('Username is required.')
            if CustomUser.objects.filter(username=username).exists():
                # Handle duplicate username case
                return HttpResponse('Username already exists.')

            form.save()
            return HttpResponse('Registration successful!')
    else:
        form = UserCreationForm()

    return render(request, 'main/registration/register.html', {'form': form})

def success(request):
    return render(request, 'main/registration/success.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'main/registration/login.html', {'form': form})

@login_required
def dashboard(request):
    ingredients = Ingredient.objects.all()
    menu_items = MenuItem.objects.all()
    return render(request, 'main/dashboard.html', {'ingredients': ingredients, 'menu_items': menu_items})


# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/index.html')
    
@login_required
def enter_ingredient(request):
    form = IngredientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return render(request, 'main/success1.html')

    ingredients = Ingredient.objects.all()
    return render(request, 'main/enter_ingredient.html', {'form': form, 'ingredients': ingredients})


@login_required   
def create_recipe(request):
    if request.method == 'POST':
        recipe_name = request.POST['recipe_name']
        ingredients = request.POST.getlist('ingredients')
        price = request.POST.get('price')

        #create RecipeRequirement
        recipe_requirement = RecipeRequirement.objects.create()
        for ing in recipe_requirement.ingredients.all():
            ingredient = Ingredient.objects.get(pk=ing.id)
            recipe_requirement.ingredients.add(ingredient)

        #create MenuItem
        menu_item = MenuItem.objects.create(
            recipe_name = recipe_name,
            recipe_requirements = recipe_requirement,
            price = price
        )
        return render(request, 'main/success.html')
    

    ingredients = Ingredient.objects.all()
    return render (request, 'main/create_recipe.html', {'ingredients': ingredients})