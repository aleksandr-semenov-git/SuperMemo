from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from memo.models import Lesson, Question, Goal, Theme, Section
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from lesson.forms import ChooseSectionForm, ChooseThemeForm, AddSectionForm, AddThemeForm


@method_decorator(login_required, name='dispatch')
class ChooseThemePage(View):
    def get(self, request, *args, **kwargs):
        goal = get_object_or_404(Goal, pk=request.session['goal_id'])
        section = get_object_or_404(Section, pk=request.session['lesson_section_id'])
        form = ChooseThemeForm(section_id=request.session['lesson_section_id'])
        return render(request, 'choose_theme.html', {'form': form, 'goal': goal, 'section': section})

    def post(self, request, *args, **kwargs):
        form = ChooseThemeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            request.session['lesson_theme_id'] = Theme.objects.get(Q(name=cd['name']),
                                                                   Q(section__id=request.session['lesson_section_id'])).id
            return redirect('lesson:sure')
        else:
            goal = get_object_or_404(Goal, pk=request.session['goal_id'])
            section = get_object_or_404(Section, pk=request.session['lesson_section_id'])
            form = ChooseThemeForm(section_id=request.session['lesson_section_id'])
            return render(request, 'choose_theme.html', {'form': form, 'goal': goal, 'section': section})


@method_decorator(login_required, name='dispatch')
class AddThemePage(View):
    def get(self, request, *args, **kwargs):
        form = AddThemeForm()
        return render(request, 'add_theme.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddThemeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            section = get_object_or_404(Section, pk=request.session['lesson_section_id'])
            theme = Theme.objects.create(name=cd['name'], section=section)
        return redirect('lesson:choose_theme')
