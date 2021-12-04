from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Entry


class LoginForm(AuthenticationForm):
    password = forms.CharField(label='AGB number')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        username = self.cleaned_data['username']
        return username.upper()


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ('forename', 'surname', 'agb_number')

    def __init__(self, category, **kwargs):
        self.category = category
        super().__init__(**kwargs)

    def save(self):
        if self.instance.pk:
            self.category.update_entry(self.instance, **self.cleaned_data)
        else:
            self.category.create_entry(**self.cleaned_data)


class MatchForm(forms.Form):
    archer_1 = forms.IntegerField(required=False)
    archer_2 = forms.IntegerField(required=False)

    def __init__(self, group, match, **kwargs):
        self.group = group
        self.match = match
        self.verified = False
        super().__init__(**kwargs)
        self.fields['archer_1'].label = match['archer_1']
        if match['score_1']:
            if match['score_1'].verified == True:
                self.verified = True
            self.fields['archer_1'].initial = match['score_1'].score
        self.fields['archer_2'].label = match['archer_2']
        if match['score_2']:
            if match['score_2'].verified == True:
                self.verified = True
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


class VerifyForm(forms.Form):
    def __init__(self, group, matches, **kwargs):
        self.group = group
        self.matches = matches
        super().__init__(**kwargs)

    def save(self):
        return self.group.verify_results(self.matches)


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


class FinalShootdownForm(forms.Form):
    score = forms.IntegerField()

    def __init__(self, archer, end, **kwargs):
        super().__init__(**kwargs)
        self.archer = archer
        self.end = end

    def save(self):
        field = 'final_match_%s_score' % self.end
        setattr(self.archer, field, self.cleaned_data['score'])
        self.archer.save()
        return self.cleaned_data['score']
