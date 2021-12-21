from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from account.forms import LoginForm, RegistrationForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        """Render login-form"""
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """Check user's post data for errors and login user"""
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['user_id'] = user.id
                    return redirect('account:profile', username=username)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:
            return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        """Logout user by request and redirect to the home-page"""
        logout(request)
        return redirect('memo:home')


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        """Render registration-form"""
        form = RegistrationForm()
        return render(request, 'registration/registration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """Check user's post data for errors and create new user. Redirect to profile-page"""
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            cd = form.cleaned_data
            new_user.username = cd['username']
            new_user.set_password(cd['password'])
            new_user.email = cd['email']
            new_user.save()
            #  --------------------------------------------------------------------------
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
            #  --------------------------------------------------------------------------
            username = cd['username']
            return redirect('account:profile', username=username)
        else:
            return render(request, 'registration/registration.html', {'form': form})
