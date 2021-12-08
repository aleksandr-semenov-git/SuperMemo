from django import forms
from lesson.models import Section, Theme, Question


class LearningForm(forms.ModelForm):
    question = forms.CharField(max_length=500, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Enter your question'}))
    answer = forms.CharField(max_length=500, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Enter the answer'}))

    class Meta:
        model = Question
        fields = ['question', 'answer']


class ChooseSectionForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Section.objects.none(),
                                  empty_label='Choose section')

    def __init__(self, *args, **kwargs):
        goal_id = kwargs.pop('goal_id', None)
        super().__init__(*args, **kwargs)

        if goal_id:
            self.fields['name'].queryset = Section.objects.filter(goal__id=goal_id)


class ChooseThemeForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Theme.objects.none(),
                                  empty_label='Choose theme')

    def __init__(self, *args, **kwargs):
        section_id = kwargs.pop('section_id', None)
        super().__init__(*args, **kwargs)

        if section_id:
            self.fields['name'].queryset = Theme.objects.filter(section__id=section_id)


class AddSectionForm(forms.ModelForm):
    name = forms.CharField(required=True, min_length=3, max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Name your section'

    class Meta:
        model = Section
        fields = ['name']


class AddThemeForm(forms.ModelForm):
    name = forms.CharField(required=True, min_length=3, max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Name your theme'

    class Meta:
        model = Theme
        fields = ['name']
