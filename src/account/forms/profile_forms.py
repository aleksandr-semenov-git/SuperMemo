from django import forms
from django.contrib.auth.forms import User


class PersonalDataEditForm(forms.ModelForm):
    username = forms.CharField(required=False, min_length=3, max_length=150)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False, min_length=3, max_length=150, label='Firstname')
    last_name = forms.CharField(required=False, min_length=3, max_length=150, label='Lastname')

    def clean(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        chd = self.changed_data
        if username == '' or email == '':
            raise forms.ValidationError('You cant leave username or email field empty')
        elif 'username' in chd and User.objects.filter(username=username).exists():
            if 'email' in chd and User.objects.filter(email=email).exists():
                raise forms.ValidationError(f'Login {username} and email {email} already exist')
            raise forms.ValidationError(f'Login {username} already exists')

        elif 'email' in chd and User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'User with email {email} already exists')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
