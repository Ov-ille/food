from django.contrib import admin

from food.models import Food, Ingredient, Recipe, Unit

# Register your models here.
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    ...

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    ...

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    ...