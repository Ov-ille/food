from django.urls import path

from . import views

app_name = "food"
urlpatterns = [
    path(
        'food_autocomplete/',
        views.FoodAutocomplete.as_view(),
        name='food-autocomplete',
    ),
    *views.RecipeView.get_urls(),
    *views.IngredientView.get_urls(),
    *views.FoodView.get_urls(),
    *views.UnitView.get_urls(),
]
