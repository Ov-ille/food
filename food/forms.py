from dal import autocomplete
from django.forms import Form, CharField, IntegerField, ModelChoiceField, ModelForm, Textarea, ValidationError

from core.forms import FormWithAddFields
from food.models import Food, Ingredient, Recipe, Unit


class EditableModelForm(ModelForm):
    """Modelform that enables displaying value of field instead of field for a readonly mode."""
    def __init__(self, editable=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not editable:
            for field_name, field in self.fields.items():
                field.is_readonly = True
                field_value = getattr(self.instance, field_name)
                field.content = field_value


class RecipeForm(EditableModelForm):

    class Meta:
        model = Recipe
        fields = "__all__"


class IngredientForm(FormWithAddFields, EditableModelForm):
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


class FoodForm(FormWithAddFields, EditableModelForm):

    class Meta:
        model = Food
        fields = "__all__"
    
    fields_can_add = ["unit"]

class UnitForm(EditableModelForm):

    class Meta:
        model = Unit
        fields = "__all__"
