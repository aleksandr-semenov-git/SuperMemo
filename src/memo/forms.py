from django import forms
from memo.models import Goal


class AddGoalForm(forms.ModelForm):
    name = forms.CharField(required=True, min_length=3, max_length=150, label='Name your goal')

    class Meta:
        model = Goal
        fields = ['name']
