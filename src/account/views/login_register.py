from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from account.forms import LoginForm, RegistrationForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        """Render page. User see LoginForm"""
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """Check data from LearningForm, log user in or show errors"""
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id
                return redirect('account:profile', username=username)
            else:
                return HttpResponse(f'Account with login {username} disabled')
        else:
            return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        """Logout user by request and redirect to the home-page"""
        logout(request)
        return redirect('memo:home')


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        """Render page. User see RegistrationForm"""
        form = RegistrationForm()
        return render(request, 'registration/registration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """Check data from RegistrationForm and create new user. Redirect to profile-page or show errors"""
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            cd = form.cleaned_data
            username = cd['username']
            new_user.username = username
            new_user.set_password(cd['password'])
            new_user.email = cd['email']
            new_user.save()
            user = authenticate(username=username, password=cd['password'])
            login(request, user)
            return redirect('account:profile', username=username)
        else:
            return render(request, 'registration/registration.html', {'form': form})
