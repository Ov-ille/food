from dal import autocomplete
from django.forms import Form, CharField, IntegerField, ModelChoiceField, ModelForm, Textarea, ValidationError

from food.models import Food, Recipe


class AddRecipeForm(ModelForm):

    # name = CharField(required=True)
    # instructions = CharField(required=False, widget=Textarea)

    class Meta:
        model = Recipe
        fields = "__all__"

class AddIngredientForm(Form):
    name = ModelChoiceField(queryset=Food.objects.all(), 
                                    widget=autocomplete.ModelSelect2(url="food-autocomplete"),
                                    required=False)
    amount = IntegerField(required=False)

    class Meta:
        widgets = {
            'name': autocomplete.Select2(url='food-autocomplete')
        }    
