from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from memo.models import Lesson, Question, Goal, Theme, Section
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from lesson.forms import ChooseSectionForm, ChooseThemeForm, AddSectionForm, AddThemeForm


@method_decorator(login_required, name='dispatch')
class ChooseSectionPage(View):
    def get(self, request, *args, **kwargs):
        # name = goal.lessons.count() + 1  # Todo Think about goal naming and query principles
        # form.fields['name'].queryset = Section.objects.filter(goal__id=request.session['goal_id'])
        # sections = goal.sections.all().values('name')
        goal = Goal.objects.get(pk=request.session['goal_id'])
        form = ChooseSectionForm(goal_id=request.session['goal_id'])
        return render(request, 'choose_section.html', {'form': form, 'goal': goal})
        # return HttpResponseRedirect(reverse('choose_chapter', kwargs={'location': location}))

    def post(self, request, *args, **kwargs):
        form = ChooseSectionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            request.session['lesson_section_id'] = Section.objects.get(name=cd['name']).id  # Todo Multiple ERROR todo 16 row
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
