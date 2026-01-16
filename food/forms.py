from django.forms import Form, CharField, Textarea


class AddRecipeForm(Form):
    name = CharField(required=True)
    instructions = CharField(required=False, widget=Textarea)