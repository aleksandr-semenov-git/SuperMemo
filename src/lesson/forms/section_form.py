from django import forms

from lesson.models import Section


class AddSectionForm(forms.ModelForm):
    """
    This is forms.ModelForm class. Class which provides naming for the new sections.

    Class attributes
    ----------------
    name : str
    """
    name = forms.CharField(required=True, min_length=3, max_length=150, label='Name your section')

    class Meta:
        model = Section
        fields = ['name']
