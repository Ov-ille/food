from dal import autocomplete
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render

from food.forms import AddIngredientForm, AddRecipeForm
from food.models import Food, Ingredient, Recipe

# Create your views here.
def add_recipe(request):
    recipe_form = AddRecipeForm(prefix="recipe")
    AddIngredientFormset = formset_factory(AddIngredientForm, extra=1)
    ingredient_formset = AddIngredientFormset(prefix="ingredient")
    context = {"recipe_form":recipe_form, "ingredient_formset": ingredient_formset}

    if request.method == "POST":
        print(request.POST)
    return HttpResponse(render(request,
                               "food/add_recipe.html",
                               context=context))
class FoodAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Food.objects.all().order_by('name')

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs