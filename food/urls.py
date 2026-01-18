from django.urls import path

from . import views

urlpatterns = [
    path(
        'food_autocomplete/',
        views.FoodAutocomplete.as_view(),
        name='food-autocomplete',
    ),
    path("add_recipe", views.add_recipe, name="add_recipe"),
]