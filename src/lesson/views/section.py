from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from lesson.forms import ChooseSectionForm, AddSectionForm
from memo.services import GoalService
from lesson.services.model_service import SectionService


@method_decorator(login_required, name='dispatch')
class ChooseSectionPage(View):
    def get(self, request, *args, **kwargs):
        goal = GoalService.get_goal_by_id(request.session['goal_id'])
        form = ChooseSectionForm(goal_id=request.session['goal_id'])
        return render(request, 'choose_section.html', {'form': form, 'goal': goal})

    def post(self, request, *args, **kwargs):
        form = ChooseSectionForm(request.POST, goal_id=request.session['goal_id'])
        if form.is_valid():
            cd = form.cleaned_data
            section = SectionService.get_section_by_name_and_goal_id(name=cd['name'],
                                                                     goal_id=request.session['goal_id'])
        else:
            goal = GoalService.get_goal_by_id(request.session['goal_id'])
            return render(request, 'choose_section.html', {'form': form, 'goal': goal})
        return redirect('lesson:choose_theme', section_id=section.id)


@method_decorator(login_required, name='dispatch')
class AddSectionPage(View):
    def get(self, request, *args, **kwargs):
        form = AddSectionForm()
        return render(request, 'add_section.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddSectionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            goal = GoalService.get_goal_by_id(request.session['goal_id'])
            section = SectionService.create_section(name=cd['name'], goal=goal)
        return redirect('lesson:choose_section')
