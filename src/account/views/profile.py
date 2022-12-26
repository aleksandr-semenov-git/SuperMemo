from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from account.forms.profile_forms import PersonalDataEditForm
from account.services.profile_service import ProfileService
from memo.forms import AddGoalForm
from memo.services import GoalService


class ProfilePage(View):
    def get(self, request, username, *args, **kwargs) -> HttpResponse:
        """Render page. User see information about his account.

        Also user see logout, edit, check-my-goals, repeat-all-questions-for-today buttons.
        User see list of his goals and add-goal button.
        """
        user = request.user
        profile = ProfileService.get_or_create_profile(user)
        goals = GoalService.get_goals_by_profile(profile)

        return render(request, 'profile_page.html', {'profile': profile,
                                                     'goals': goals,
                                                     'username': username})


@method_decorator(login_required, name='dispatch')
class AddGoalPage(View):
    def get(self, request, *args, **kwargs):
        """Render page. User see AddGoalForm and fill it in"""
        form = AddGoalForm()
        return render(request, 'add_goal.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """Redirect user to the my_goals page. Validate the form"""
        form = AddGoalForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            profile = request.user.profile
            GoalService.create_goal(cd['name'], profile)
        return redirect('account:profile_basic')


class ProfilePageBasic(View):
    def get(self, request, *args, **kwargs) -> HttpResponseRedirect:
        """Redirect to user's profile or redirect to login"""
        if request.user.is_authenticated:
            return redirect('account:profile', username=request.user.username)
        else:
            return redirect('account:login')


@method_decorator(login_required, name='dispatch')
class EditPage(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Render page. User see PersonalDataEditForm filled in with his information and submit button.

        Also user see edit-password button.
        """
        user = request.user
        form = PersonalDataEditForm(initial={'username': user.username,
                                             'email': user.email,
                                             'first_name': user.first_name,
                                             'last_name': user.last_name},
                                    )
        return render(request, 'edit.html', {'form': form})

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Check data from PersonalDataEditForm. Redirect to the profile-page or show errors"""
        form = PersonalDataEditForm(request.POST, instance=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            form.save(commit=True)
            return redirect('account:profile', username=username)
        return render(request, 'edit.html', {'form': form})
