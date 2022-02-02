from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from account.forms.profile_forms import PersonalDataEditForm
from memo.services import GoalService
from account.services.profile_service import ProfileService


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
