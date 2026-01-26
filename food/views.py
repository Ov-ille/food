from dal import autocomplete
from django.forms import BaseModelFormSet, formset_factory, inlineformset_factory, modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from food.forms import FoodForm, IngredientForm, RecipeForm
from food.models import Food, Ingredient, Recipe, Unit


# Create your views here.
def recipe_list(request):
    return HttpResponse(render(request,
                               "food/recipe_list.html",
                               context={"recipes": Recipe.objects.all()}))


def add_change_recipe(request, recipe_id=None):
    add = recipe_id is None

    # edit: currently in edit mode
    # editable: can edit
    # has_change_permission: can edit
    editable = False
    if request.GET.get("e", 0) == "1" or add:
        editable = True

    # todo: permissions
    has_change_permission = True
    has_delete_permission = True
    has_add_permission = True

    if not has_change_permission:
        editable = False

    if add:
        recipe = None
    else:
        try:
            recipe_id = int(recipe_id)
            recipe = Recipe.objects.get(pk=recipe_id)
        except (ValueError, Recipe.DoesNotExist):
            # todo
            raise Exception("Cant parse ID or Object does not exist!")

    if request.method == "GET":
        recipe_form = RecipeForm(prefix="recipe", instance=recipe)
        IngredientFormset = inlineformset_factory(
            Recipe, 
            Ingredient, 
            IngredientForm, 
            extra=0,    
            can_delete=editable and has_delete_permission, 
            validate_max=True
            )
        ingredient_formset = IngredientFormset(
            prefix="ingredient", 
            instance=recipe, 
            queryset=Ingredient.objects.none() if not recipe else None
            )
        
        if not editable:
            for field_name, field in recipe_form.fields.items():
                field.is_readonly = True
                field_value = getattr(recipe_form.instance, field_name)
                field.content = field_value
            for form in ingredient_formset:
                for field_name, field in form.fields.items():
                    if form.instance.id and field_name in [f.name for f in form.instance._meta.get_fields()]:
                        field.is_readonly = True
                        field_value = getattr(form.instance, field_name)
                        field.content = field_value

    elif request.method == "POST":
        recipe_form = RecipeForm(
            prefix="recipe", 
            data=request.POST, 
            instance=recipe if not add else None
            )
        recipe_form_validated = recipe_form.is_valid()

        if recipe_form_validated:
            new_recipe = recipe_form.save(commit=False)
        else:
            new_recipe = recipe_form.instance

        IngredientFormset = inlineformset_factory(
            Recipe, 
            Ingredient, 
            IngredientForm, 
            extra=0, 
            can_delete=editable and has_delete_permission, 
            validate_max=True
            )
        ingredient_formset = IngredientFormset(
            prefix="ingredient", 
            data=request.POST, 
            instance=recipe if not add else None
            )
        ingredient_formset_validated = ingredient_formset.is_valid()
        if ingredient_formset_validated and recipe_form_validated:
            recipe_form.save()
            ingredient_formset.instance = new_recipe
            ingredient_formset.save()
            return HttpResponseRedirect(reverse("change_recipe", kwargs={"recipe_id": new_recipe.id}))

    context = {
        "recipe_form": recipe_form, 
        "ingredient_formset": ingredient_formset, 
        "food_form": FoodForm(),
        "add": add, 
        "editable": editable
    }

    return HttpResponse(render(request,
                               "food/add_change_recipe.html",
                               context=context))

def add_food(request):
    if request.POST:
        food_form = FoodForm(
            data=request.POST, 
        )
        food_form_validated = food_form.is_valid()
        if food_form_validated:
            food = Food.objects.create(name=food_form.instance.name, unit=food_form.instance.unit)
            return JsonResponse({"id": food.pk, "text": food.name})
        else:
            return JsonResponse({"errors": food_form.errors})

class FoodAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # todo: permissions
        qs = Food.objects.all().order_by('name')

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs