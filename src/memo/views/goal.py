from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from memo.forms import AddGoalForm
from memo.services import GoalService


@method_decorator(login_required, name='dispatch')
class GoalPage(View):
    def get(self, request, *args, **kwargs):
        """"""
        goal = GoalService.get_goal_by_id(kwargs['goal_id'])
        request.session['goal_id'] = kwargs['goal_id']
        return render(request, 'goal_page.html', {'goal': goal})


@method_decorator(login_required, name='dispatch')
class AddGoalPage(View):
    def get(self, request, *args, **kwargs):
        """"""
        form = AddGoalForm()
        return render(request, 'add_goal.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """"""
        form = AddGoalForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            profile = request.user.profile
            GoalService.create_goal(cd['name'], profile)
        return redirect('memo:my_goals')


@method_decorator(login_required, name='dispatch')
class MyGoalsPage(View):
    def get(self, request, *args, **kwargs):
        """"""
        goals = GoalService.get_goals_by_profile(profile=request.user.profile)
        return render(request, 'my_goals.html', {'goals': goals})
