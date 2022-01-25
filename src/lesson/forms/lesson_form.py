from django import forms
from lesson.models import Question


class AddEditQuestionForm(forms.ModelForm):
    question = forms.CharField(max_length=500, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Enter your question'}))
    answer = forms.CharField(max_length=500, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Enter the answer'}))

    class Meta:
        model = Question
        fields = ['question', 'answer']
