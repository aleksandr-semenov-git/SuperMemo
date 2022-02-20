from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import LessonLearnPage, AddThemePage, AddSectionPage, EditQuestionPage, DeleteQuestionView

urlpatterns = [
    path('add-section/', AddSectionPage.as_view(), name='add_section'),
    path('add-theme/<int:section_id>', AddThemePage.as_view(), name='add_theme'),
    path('learn/<int:theme_id>', LessonLearnPage.as_view(), name='lesson_learn'),
    path('learn/edit_question/<int:question_id>', EditQuestionPage.as_view(), name='edit_question'),
    path('learn/delete_question/<int:question_id>', DeleteQuestionView.as_view(), name='delete_question'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
