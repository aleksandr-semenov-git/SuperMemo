from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import LessonLearnPage, AddThemePage, ChooseThemePage, AddSectionPage, ChooseSectionPage
from .views.lesson import EditQuestionPage, DeleteQuestionView, LessonRepeat, LessonRepeatCheck

urlpatterns = [

    path('new-lesson/choose-section/', ChooseSectionPage.as_view(), name='choose_section'),
    path('new-lesson/choose-theme/<int:section_id>', ChooseThemePage.as_view(), name='choose_theme'),
    path('new-lesson/add-section/', AddSectionPage.as_view(), name='add_section'),
    path('new-lesson/add-theme/<int:section_id>', AddThemePage.as_view(), name='add_theme'),
    path('learning-page/<int:theme_id>', LessonLearnPage.as_view(), name='lesson_learn'),
    path('learning-page/edit_question/<int:question_id>', EditQuestionPage.as_view(), name='edit_question'),
    path('learning-page/delete_question/<int:question_id>', DeleteQuestionView.as_view(), name='delete_question'),
    path('learning-page/repeat/<int:theme_id>', LessonRepeat.as_view(), name='lesson_repeat'),
    path('learning-page/repeat/check/<int:theme_id>', LessonRepeatCheck.as_view(), name='lesson_repeat_check'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
