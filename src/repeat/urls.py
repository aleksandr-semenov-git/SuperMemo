from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import RepeatTheme, Repeat, RepeatCheck, RepeatMix, RepeatSection, RepeatGoal, NotRemember, Remember

urlpatterns = [
    path('mix/', RepeatMix.as_view(), name='repeat_mix'),
    path('goal/<int:goal_id>', RepeatGoal.as_view(), name='repeat_goal'),
    path('section/<int:section_id>', RepeatSection.as_view(), name='repeat_section'),
    path('theme/<int:theme_id>', RepeatTheme.as_view(), name='repeat_theme'),
    path('<int:rep_id>/', Repeat.as_view(), name='repeat'),
    path('check/<int:question_id>', RepeatCheck.as_view(), name='repeat_check'),
    path('remember/<int:question_id>', Remember.as_view(), name='remember'),
    path('not_remember/<int:question_id>', NotRemember.as_view(), name='not_remember'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



