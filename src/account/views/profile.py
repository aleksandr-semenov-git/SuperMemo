from account.functions import profile_exists, create_profile, get_goals_by_profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from memo.models import Profile, Goal, Question, Theme, Section
from memo.forms import PersonalDataEditForm, AddGoalForm


class ProfilePage(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not profile_exists(user):
            profile = create_profile(user)
        else:
            profile = user.profile
        goals = get_goals_by_profile(profile)

        return render(request, 'profile_page.html', {'profile': profile,
                                                     'goals': goals,
                                                     'username': kwargs['username']})


class ProfilePageBasic(View):
    """Build url to user's profile or redirect to login"""
    def get(self, request, *args, **kwargs):
        username = request.user.username
        if username:
            return redirect('account:profile', username=username)
        else:
            return redirect('account:login')


@method_decorator(login_required, name='dispatch')
class EditPage(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        form = PersonalDataEditForm(initial={'username': user.username,
                                             'email': user.email,
                                             'first_name': user.first_name,
                                             'last_name': user.last_name},
                                    )
        return render(request, 'edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PersonalDataEditForm(request.POST, instance=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            user = form.save(commit=True)
            return redirect('account:profile', username=username)
        return render(request, 'edit.html', {'form': form})
