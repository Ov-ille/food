from django.urls import path

from . import views

urlpatterns = [
    path("add_recipe", views.add_recipe, name="add_recipe"),
]