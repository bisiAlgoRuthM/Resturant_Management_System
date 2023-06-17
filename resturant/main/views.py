from django.shortcuts import render
from django.http import JsonResponse
from django.views import View #import generic view clas
from .models import RecipeRequirement, MenuItem, Ingredient
from .forms import IngredientForm

# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/index.html')
    

def enter_ingredient(request):
    form = IngredientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return render(request, 'main/success1.html')

    ingredients = Ingredient.objects.all()
    return render(request, 'main/enter_ingredent.html', {'form': form, 'ingredients': ingredients})


    
def create_recipe(request):
    if request.method == 'POST':
        recipe_name = request.POST('recipe_name')
        ingredients = request.POST.getlist('ingredients')
        price = request.POST.get('price')

        #create RecipeRequirement
        recipe_requirement = RecipeRequirement.objects.create()
        for ingredient in recipe_requirement.ingredents:
            ingredient = Ingredient.objects.get(pk=ingredient.id)
            recipe_requirement.ingredients.add(ingredient)

        #create MenuItem
        menu_item = MenuItem.objects.create(
            recipe_name = recipe_name,
            recipe_requirement = recipe_requirement,
            price = price
        )
        return render(request, 'main/success.html')
    

    ingredients = Ingredient.objects.all()
    return render (request, 'main/create_recipe.html', {'ingredients': ingredients})