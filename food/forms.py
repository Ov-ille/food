from dal import autocomplete
from django.forms import Form, CharField, IntegerField, ModelChoiceField, ModelForm, Textarea, ValidationError

from food.models import Food, Ingredient, Recipe


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = "__all__"

class IngredientForm(ModelForm):
    food = ModelChoiceField(queryset=Food.objects.all(), 
                                    widget=autocomplete.ModelSelect2(url="food-autocomplete"),
                                    required=True)

    class Meta:
        model = Ingredient
        fields = "__all__"
        widgets = {
            'food': autocomplete.Select2(url='food-autocomplete')
        }