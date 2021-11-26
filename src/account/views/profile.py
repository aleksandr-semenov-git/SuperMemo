from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from memo.models import Profile, Goal, Question, Theme, Section
from memo.forms import PersonalDataEditForm, AddGoalForm

# all_lessons = Lesson.objects.filter(goal__profile=profile)
# theme_lessons = my_theme.section.goal.lessons


class ProfilePage(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        profile_exists = Profile.objects.filter(user=user).exists()
        if not profile_exists:  # Todo create_profile(user)
            profile = Profile.objects.create(
                user=request.user
            )
        else:
            profile = user.profile
        goals = profile.goals.all()  # Todo get_goals_by_profile(profile)

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
