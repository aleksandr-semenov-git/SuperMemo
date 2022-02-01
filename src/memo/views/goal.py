from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from memo.forms import AddGoalForm
from memo.services import GoalService


@method_decorator(login_required, name='dispatch')
class MyGoalsPage(View):
    def get(self, request, *args, **kwargs):
        """Render page. User see all he's goals"""
        goals = GoalService.get_goals_by_profile(profile=request.user.profile)
        return render(request, 'my_goals.html', {'goals': goals})


@method_decorator(login_required, name='dispatch')
class GoalPage(View):
    def get(self, request, goal_id, *args, **kwargs):
        """Render page. User see details of the goal"""
        goal = GoalService.get_goal_by_id(goal_id)
        request.session['goal_id'] = goal_id
        return render(request, 'goal_page.html', {'goal': goal})


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
        return redirect('memo:my_goals')
