from django import forms

from lesson.models import Question


class AddEditQuestionForm(forms.ModelForm):
    """
    Class which is used for add or edit questions and answers.

    Class attributes
    ----------------
    question : str
    answer : str
    """
    question = forms.CharField(max_length=500, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Enter your question'}))
    answer = forms.CharField(max_length=500, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Enter the answer'}))

    class Meta:
        model = Question
        fields = ['question', 'answer']
