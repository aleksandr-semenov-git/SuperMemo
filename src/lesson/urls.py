from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import LessonLearnPage, AddThemePage, ChooseThemePage, AddSectionPage, ChooseSectionPage


urlpatterns = [

    path('new-lesson/choose-section/', ChooseSectionPage.as_view(), name='choose_section'),
    path('new-lesson/choose-theme/<int:section_id>', ChooseThemePage.as_view(), name='choose_theme'),
    path('new-lesson/add-section/', AddSectionPage.as_view(), name='add_section'),
    path('new-lesson/add-theme/<int:section_id>', AddThemePage.as_view(), name='add_theme'),
    path('learning-page/<int:theme_id>', LessonLearnPage.as_view(), name='lesson_learn'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
