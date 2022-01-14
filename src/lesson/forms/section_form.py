from django import forms
from lesson.models import Section


class AddSectionForm(forms.ModelForm):
    name = forms.CharField(required=True, min_length=3, max_length=150, label='Name your section')

    class Meta:
        model = Section
        fields = ['name']


class ChooseSectionForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Section.objects.none(),
                                  empty_label='Choose section')

    def __init__(self, *args, **kwargs):
        goal_id = kwargs.pop('goal_id', None)
        super().__init__(*args, **kwargs)

        if goal_id:
            self.fields['name'].queryset = Section.objects.filter(goal__id=goal_id)