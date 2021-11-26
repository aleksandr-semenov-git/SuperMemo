from django import forms
from django.contrib.auth.forms import User
from .models import Profile, Goal, Question, Section, Theme


class PersonalDataEditForm(forms.ModelForm):
    username = forms.CharField(required=False, min_length=3, max_length=150, )
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False, min_length=3, max_length=150)
    last_name = forms.CharField(required=False, min_length=3, max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Firstname'
        self.fields['last_name'].label = 'Lastname'

    def clean(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        chd = self.changed_data
        if 'username' in chd and User.objects.filter(username=username).exists():
            if User.objects.filter(email=email).exists() and 'email' in chd:
                raise forms.ValidationError(f'Login {username} and email {email} are already exist')
            raise forms.ValidationError(f'Login {username} is already exist')

        elif 'email' in chd and User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'User with email {email} is already exist')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class AddGoalForm(forms.ModelForm):
    name = forms.CharField(required=True, min_length=3, max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Name your goal'

    class Meta:
        model = Goal
        fields = ['name']
