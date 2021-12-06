from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import LessonPage, EndLessonPage, AddThemePage, ChooseThemePage, AddSectionPage, ChooseSectionPage
from .views import SurePage, MyLessonsPage


urlpatterns = [

    path('my-lessons/', MyLessonsPage.as_view(), name='my_lessons'),
    path('new-lesson/choose-section/', ChooseSectionPage.as_view(), name='choose_section'),
    path('new-lesson/choose-theme/<int:section_id>', ChooseThemePage.as_view(), name='choose_theme'),
    path('new-lesson/add-section/', AddSectionPage.as_view(), name='add_section'),
    path('new-lesson/add-theme/<int:section_id>', AddThemePage.as_view(), name='add_theme'),
    path('new-lesson/confirm/<int:theme_id>', SurePage.as_view(), name='sure'),
    path('learning-page/', LessonPage.as_view(), name='lesson_page'),
    path('learning-page/end-lesson/', EndLessonPage.as_view(), name='end_lesson'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
