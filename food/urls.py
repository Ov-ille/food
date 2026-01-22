from django.urls import path

from . import views

urlpatterns = [
    path(
        'food_autocomplete/',
        views.FoodAutocomplete.as_view(),
        name='food-autocomplete',
    ),
    path("recipe/add", views.add_change_recipe, name="add_recipe"),
    path("recipe/<path:recipe_id>/change", views.add_change_recipe, name="change_recipe"),
    path("recipe/", views.recipe_list, name="recipe_list"),
]