from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import RepeatTheme, Repeat, RepeatCheck, RepeatMix, RepeatSection, RepeatGoal

urlpatterns = [
    path('learning-page/repeat/mix/', RepeatMix.as_view(), name='repeat_mix'),
    path('learning-page/repeat/goal/<int:goal_id>', RepeatGoal.as_view(), name='repeat_goal'),
    path('learning-page/repeat/section/<int:section_id>', RepeatSection.as_view(), name='repeat_section'),
    path('learning-page/repeat/theme/<int:theme_id>', RepeatTheme.as_view(), name='repeat_theme'),

    path('learning-page/repeat/<int:rep_id>', Repeat.as_view(), name='repeat'),
    path('learning-page/repeat/check/<int:question_id>', RepeatCheck.as_view(), name='repeat_check'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



