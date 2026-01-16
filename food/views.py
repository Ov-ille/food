from django.http import HttpResponse
from django.shortcuts import render

from food.forms import AddRecipeForm

# Create your views here.
def add_recipe(request):
    form = AddRecipeForm()
    context = {"form":form}
    return HttpResponse(render(request,
                               "food/add_recipe.html",
                               context=context))