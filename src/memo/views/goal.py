from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_POST
from memo.decorators import TestMixin1
from memo.models import Profile, Goal, Question, Theme, Section
from django.contrib.auth.models import User
from memo.forms import AddGoalForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


@method_decorator(login_required, name='dispatch')
class GoalPage(View):  # Todo: decorator user_passes_test
    def get(self, request, *args, **kwargs):
        goal = Goal.objects.get(pk=kwargs['goal_id'])
        request.session['goal_id'] = kwargs['goal_id']
        return render(request, 'goal_page.html', {'goal': goal})


@method_decorator(login_required, name='dispatch')
class AddGoalPage(View):
    def get(self, request, *args, **kwargs):
        form = AddGoalForm()
        return render(request, 'add_goal.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddGoalForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            profile = request.user.profile
            goal = Goal.objects.create(name=cd['name'], profile=profile)
        return redirect('account:profile_basic')
