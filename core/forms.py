from django.urls import reverse


class FormWithAddFields():

    fields_can_add = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_fields_can_add()

    def set_fields_can_add(self):
        for field_name, field in self.fields.items():
            # todo: check if field is a foreignkey and can actually add data there!
            # todo: refactor the whole thing somehow
            if field_name in self.fields_can_add:
                field.can_add = True
                self.set_add_url(field, field_name)
    
    def set_add_url(self, field, field_name):
        if getattr(self._meta, "model", False):
            app_name = self._meta.model._meta.app_label
            field.add_url = reverse(f"{app_name}:{field_name}_add") + "?p=1"