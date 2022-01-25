from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import RepeatTheme, RepeatCheck, RepeatMix, RepeatSection, RepeatGoal

urlpatterns = [
    # path('learning-page/repeat/', RepeatMix.as_view(), name='lesson_repeat_mix'),
    # path('learning-page/repeat/<int:goal_id>', RepeatGoal.as_view(), name='lesson_repeat_goal'),
    # path('learning-page/repeat/<int:section_id>', RepeatSection.as_view(), name='lesson_repeat_section'),
    path('learning-page/repeat/<int:theme_id>', RepeatTheme.as_view(), name='repeat_theme'),
    path('learning-page/repeat/check/<int:question_id>', RepeatCheck.as_view(), name='repeat_check'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



