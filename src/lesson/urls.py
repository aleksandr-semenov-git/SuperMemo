from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import LessonLearnPage, AddThemePage, ChooseThemePage, AddSectionPage, ChooseSectionPage, EditQuestionPage,\
    DeleteQuestionView

urlpatterns = [
    path('choose-section/', ChooseSectionPage.as_view(), name='choose_section'),
    path('choose-theme/<int:section_id>', ChooseThemePage.as_view(), name='choose_theme'),
    path('add-section/', AddSectionPage.as_view(), name='add_section'),
    path('add-theme/<int:section_id>', AddThemePage.as_view(), name='add_theme'),
    path('learn/<int:theme_id>', LessonLearnPage.as_view(), name='lesson_learn'),
    path('learn/edit_question/<int:question_id>', EditQuestionPage.as_view(), name='edit_question'),
    path('learn/delete_question/<int:question_id>', DeleteQuestionView.as_view(), name='delete_question'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
