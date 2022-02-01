from django import forms

from lesson.models import Theme


class AddThemeForm(forms.ModelForm):
    """
    This is forms.ModelForm class. Class which provides naming for the new themes.

    Class attributes
    ----------------
    name : str
    """
    name = forms.CharField(required=True, min_length=3, max_length=150, label='Name your theme')

    class Meta:
        model = Theme
        fields = ['name']


class ChooseThemeForm(forms.Form):
    """
    This is forms.Form class. Class which construct dropdown menu where user will chose one theme

    Class attributes
    ----------------
    name : ModelChoiceField

    Methods
    -------
    __init__(self, *args, **kwargs)
        this method takes parameter section_id from the kwargs and provide required queryset as choices
    """
    name = forms.ModelChoiceField(queryset=Theme.objects.none(),
                                  empty_label='Choose theme')

    def __init__(self, *args, **kwargs):
        section_id = kwargs.pop('section_id', None)
        super().__init__(*args, **kwargs)

        if section_id:
            self.fields['name'].queryset = Theme.objects.filter(section__id=section_id)
