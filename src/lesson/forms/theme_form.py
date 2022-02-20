from django import forms

from lesson.models import Theme


class AddThemeForm(forms.ModelForm):
    """
    Class which provides naming for the new themes.

    Class attributes
    ----------------
    name : str
    """
    name = forms.CharField(required=True, min_length=3, max_length=150, label='Name your theme')

    class Meta:
        model = Theme
        fields = ['name']
