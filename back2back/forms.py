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
        if self.instance.pk:
            self.instance.save()
        else:
            self.category.create_entry(**self.cleaned_data)


class MatchForm(forms.Form):
    archer_1 = forms.IntegerField(required=False)
    archer_2 = forms.IntegerField(required=False)

    def __init__(self, group, match, **kwargs):
        self.group = group
        self.match = match
        super().__init__(**kwargs)
        self.fields['archer_1'].label = match['archer_1']
        self.fields['archer_2'].label = match['archer_2']

    def save(self):
        self.group.record_result(match, self.cleaned_data)
