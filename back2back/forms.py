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
        if match['score_1']:
            self.fields['archer_1'].initial = match['score_1'].score
        self.fields['archer_2'].label = match['archer_2']
        if match['score_2']:
            self.fields['archer_2'].initial = match['score_2'].score

    def clean(self):
        if 'archer_1' in self.cleaned_data and 'archer_2' in self.cleaned_data:
            a1 = self.cleaned_data['archer_1']
            a2 = self.cleaned_data['archer_2']
            if (a1 is None and a2 is not None) or (a1 is not None and a2 is None):
                raise forms.ValidationError('Please record one result or neither.')
        return self.cleaned_data

    def save(self):
        return self.group.record_result(self.match, self.cleaned_data)


class FinalMatchForm(MatchForm):
    archer_1 = forms.IntegerField(required=False)
    archer_2 = forms.IntegerField(required=False)

    def __init__(self, category, match, **kwargs):
        self.category = category
        self.match = match
        forms.Form.__init__(self, **kwargs)
        self.fields['archer_1'].label = match['archer_1']
        if match['score_1']:
            self.fields['archer_1'].initial = match['score_1']
        self.fields['archer_2'].label = match['archer_2']
        if match['score_2']:
            self.fields['archer_2'].initial = match['score_2']

    def save(self):
        self.category.record_final_result(self.match, self.cleaned_data)
