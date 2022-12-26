from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from lesson.forms import AddThemeForm
from lesson.services import SectionService
from lesson.services.theme_service import ThemeService


@method_decorator(login_required, name='dispatch')
class AddThemePage(View):
    def get(self, request, *args, **kwargs):
        """Render page. User see AddThemeForm, logout and submit buttons"""
        form = AddThemeForm()
        return render(request, 'add_theme.html', {'form': form})

    def post(self, request, section_id, *args, **kwargs):
        """Check data from AddThemeForm and redirect to the goal-page or show form errors"""
        form = AddThemeForm(request.POST)
        section = SectionService.get_section_by_id(section_id)
        goal_id = request.session['goal_id']
        if form.is_valid():
            cd = form.cleaned_data
            theme = ThemeService.create_theme(name=cd['name'], section=section)
            return redirect('memo:goal_page', goal_id=goal_id)
        return render(request, 'add_theme.html', {'form': form})
