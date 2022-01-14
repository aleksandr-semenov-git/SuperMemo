from django import forms
from lesson.models import Theme


class AddThemeForm(forms.ModelForm):
    name = forms.CharField(required=True, min_length=3, max_length=150, label='Name your theme')

    class Meta:
        model = Theme
        fields = ['name']


class ChooseThemeForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Theme.objects.none(),
                                  empty_label='Choose theme')

    def __init__(self, *args, **kwargs):
        section_id = kwargs.pop('section_id', None)
        super().__init__(*args, **kwargs)

        if section_id:
            self.fields['name'].queryset = Theme.objects.filter(section__id=section_id)
