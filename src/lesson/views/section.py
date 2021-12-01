from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from lesson.forms import ChooseSectionForm, ChooseThemeForm, AddSectionForm, AddThemeForm
from memo.models import Lesson, Question, Goal, Theme, Section


@method_decorator(login_required, name='dispatch')
class ChooseSectionPage(View):
    def get(self, request, *args, **kwargs):
        goal = get_object_or_404(Goal, pk=request.session['goal_id'])
        form = ChooseSectionForm(goal_id=request.session['goal_id'])
        return render(request, 'choose_section.html', {'form': form, 'goal': goal})

    def post(self, request, *args, **kwargs):
        form = ChooseSectionForm(request.POST, goal_id=request.session['goal_id'])
        if form.is_valid():
            cd = form.cleaned_data
            request.session['lesson_section_id'] = Section.objects.get(Q(name=cd['name']),
                                                                       Q(goal__id=request.session['goal_id'])).id
        else:
            goal = get_object_or_404(Goal, pk=request.session['goal_id'])
            return render(request, 'choose_section.html', {'form': form, 'goal': goal})
        return redirect('lesson:choose_theme')


@method_decorator(login_required, name='dispatch')
class AddSectionPage(View):
    def get(self, request, *args, **kwargs):
        form = AddSectionForm()
        return render(request, 'add_section.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddSectionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            goal = Goal.objects.get(pk=request.session['goal_id'])
            section = Section.objects.create(name=cd['name'], goal=goal)
        return redirect('lesson:choose_section')
