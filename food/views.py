from dal import autocomplete
from django.forms import BaseModelFormSet, formset_factory, inlineformset_factory, modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render

from food.forms import AddIngredientForm, AddRecipeForm
from food.models import Food, Ingredient, Recipe


# Create your views here.
def add_recipe(request):
    recipe_form = AddRecipeForm(prefix="recipe")
    AddIngredientFormset = inlineformset_factory(Recipe, Ingredient, AddIngredientForm, extra=1, max_num=2, can_delete=True, validate_max=True)
    ingredient_formset = AddIngredientFormset(prefix="ingredient", queryset=Ingredient.objects.none())


    if request.method == "POST":
        recipe_form = AddRecipeForm(prefix="recipe", data=request.POST)
        recipe_form_validated = recipe_form.is_valid()

        if recipe_form_validated:
            new_recipe = recipe_form.save(commit=False)
        else:
            new_recipe = recipe_form.instance

        ingredient_formset = AddIngredientFormset(prefix="ingredient", data=request.POST)
        ingredient_formset_validated = ingredient_formset.is_valid()

        if ingredient_formset_validated and recipe_form_validated:
            new_recipe.save()
            recipe_form.save_m2m()
            ingredient_formset.instance = new_recipe
            ingredient_formset.save()
        else:
            recipe_form_validated = False
    
    context = {"recipe_form":recipe_form, "ingredient_formset": ingredient_formset}

    

    return HttpResponse(render(request,
                               "food/add_recipe.html",
                               context=context))


class FoodAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Food.objects.all().order_by('name')

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs