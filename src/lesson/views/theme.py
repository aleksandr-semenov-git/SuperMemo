from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from lesson.forms import ChooseThemeForm, AddThemeForm
from memo.services import GoalService, SectionService, ThemeService


@method_decorator(login_required, name='dispatch')
class ChooseThemePage(View):
    def get(self, request, *args, **kwargs):
        goal = GoalService.get_goal_by_id(request.session['goal_id'])
        section = SectionService.get_section_by_id(section_id=kwargs['section_id'])
        form = ChooseThemeForm(section_id=kwargs['section_id'])
        return render(request, 'choose_theme.html', {'form': form, 'goal': goal, 'section': section})

    def post(self, request, *args, **kwargs):
        form = ChooseThemeForm(request.POST, section_id=kwargs['section_id'])
        if form.is_valid():
            cd = form.cleaned_data
            theme = ThemeService.get_theme_by_name_and_section_id(name=cd['name'],
                                                                  section_id=kwargs['section_id'])
            request.session['theme_id'] = theme.id
            return redirect('lesson:sure', theme_id=theme.id)
        else:
            goal = GoalService.get_goal_by_id(request.session['goal_id'])
            section = SectionService.get_section_by_id(kwargs['section_id'])
            form = ChooseThemeForm(section_id=kwargs['section_id'])
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
            section = SectionService.get_section_by_id(kwargs['section_id'])
            theme = ThemeService.create_theme(name=cd['name'], section=section)
        return redirect('lesson:choose_theme', section_id=section.id)
