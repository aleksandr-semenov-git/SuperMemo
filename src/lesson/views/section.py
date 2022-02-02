from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from lesson.forms import AddSectionForm
from lesson.services import SectionService
from memo.services import GoalService


@method_decorator(login_required, name='dispatch')
class AddSectionPage(View):
    def get(self, request, *args, **kwargs):
        """Render page. User see AddSectionForm, logout and submit buttons"""
        form = AddSectionForm()
        return render(request, 'add_section.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """Check data from AddSectionForm and redirect to the goal-page. Show form errors if needed"""
        form = AddSectionForm(request.POST)
        goal_id = request.session['goal_id']
        if form.is_valid():
            cd = form.cleaned_data
            goal = GoalService.get_goal_by_id(request.session['goal_id'])
            section = SectionService.create_section(name=cd['name'], goal=goal)
            return redirect('memo:goal_page', goal_id=goal_id)
        return render(request, 'add_section.html', {'form': form})
