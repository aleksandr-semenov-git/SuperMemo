from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
    username = forms.CharField(min_length=3, max_length=20, required=True, label='Login')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'User with login {username} not found.')
        return username

    def clean_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
        return password

    def clean(self):
        super().clean()

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(min_length=3, max_length=20, required=True, label='Login')
    password = forms.CharField(widget=forms.PasswordInput, required=True, max_length=20, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, max_length=20,
                                       label='Confirm password')
    email = forms.EmailField(required=True, label='Email')

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['net']:
            raise forms.ValidationError('Registration for domain "net" is impossible')
        elif User.objects.filter(email=email).exists():
            raise forms.ValidationError('Current email is already registered')
        else:
            return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Current username {username} is already registered')
        else:
            return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords not match')
        else:
            return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email']
