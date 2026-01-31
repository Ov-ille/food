from dal import autocomplete
from django.forms import Form, CharField, IntegerField, ModelChoiceField, ModelForm, Textarea, ValidationError

from core.forms import FormWithAddFields
from food.models import Food, Ingredient, Recipe, Unit


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = "__all__"


class IngredientForm(FormWithAddFields, ModelForm):
    food = ModelChoiceField(queryset=Food.objects.all(), 
                                    widget=autocomplete.ModelSelect2(url="food:food-autocomplete"),
                                    required=True)

    class Meta:
        model = Ingredient
        fields = "__all__"
        widgets = {
            'food': autocomplete.Select2(url='food:food-autocomplete')
        }

    fields_can_add = ["food"]



class FoodForm(FormWithAddFields, ModelForm):

    class Meta:
        model = Food
        fields = "__all__"
    
    fields_can_add = ["unit"]

class UnitForm(ModelForm):

    class Meta:
        model = Unit
        fields = "__all__"
    
