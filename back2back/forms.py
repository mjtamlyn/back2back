from django import forms

from .models import Entry


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ('name', 'agb_number', 'seeding')

    def __init__(self, category, **kwargs):
        self.category = category
        super().__init__(**kwargs)

    def save(self):
        self.category.create_entry(**self.cleaned_data)
