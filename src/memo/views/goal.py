from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from memo.services import GoalService


@method_decorator(login_required, name='dispatch')
class GoalPage(View):
    def get(self, request, goal_id, *args, **kwargs):
        """Render page. User see details of the goal"""
        goal = GoalService.get_goal_by_id(goal_id)
        request.session['goal_id'] = goal_id
        return render(request, 'goal_page.html', {'goal': goal})
