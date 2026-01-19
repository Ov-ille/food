from django.urls import path

from . import views

urlpatterns = [
    path(
        'food_autocomplete/',
        views.FoodAutocomplete.as_view(),
        name='food-autocomplete',
    ),
    path("recipe/", views.recipe_list, name="recipe_list"),
]