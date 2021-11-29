from memo.services import ProfileService, GoalService
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from memo.forms import PersonalDataEditForm


class ProfilePage(View):
    def get(self, request, *args, **kwargs):
        """Get or create user's profile
        get profile's goals
        display profile's attributes and goals
        """
        user = request.user
        profile = ProfileService.get_or_create_profile(user)
        goals = GoalService.get_goals_by_profile(profile)

        return render(request, 'profile_page.html', {'profile': profile,
                                                     'goals': goals,
                                                     'username': kwargs['username']})


class ProfilePageBasic(View):
    def get(self, request, *args, **kwargs):
        """Redirect to user's profile or redirect to login"""
        if request.user.is_authenticated:
            return redirect('account:profile', username=request.user.username)
        else:
            return redirect('account:login')


@method_decorator(login_required, name='dispatch')
class EditPage(View):
    def get(self, request, *args, **kwargs):
        """Prepare and display the form with user's data"""
        user = request.user
        form = PersonalDataEditForm(initial={'username': user.username,
                                             'email': user.email,
                                             'first_name': user.first_name,
                                             'last_name': user.last_name},
                                    )
        return render(request, 'edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """Redirect to profile-page if the form is valid or refresh edit-page and show errors messages"""
        form = PersonalDataEditForm(request.POST, instance=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            form.save(commit=True)
            return redirect('account:profile', username=username)
        return render(request, 'edit.html', {'form': form})
