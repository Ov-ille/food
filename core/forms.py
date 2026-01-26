class FormWithAddFields():

    fields_can_add = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_fields_can_add()

    def set_fields_can_add(self):
        for field_name, field in self.fields.items():
            if field_name in self.fields_can_add:
                field.can_add = True