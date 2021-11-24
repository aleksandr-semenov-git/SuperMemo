from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import LessonPage, EndLessonPage, AddThemePage, ChooseThemePage, AddSectionPage, ChooseSectionPage
from .views import SurePage

SurePage


urlpatterns = [

    path('new-lesson/choose_section/', ChooseSectionPage.as_view(), name='choose_section'),
    path('new-lesson/choose_theme/', ChooseThemePage.as_view(), name='choose_theme'),
    path('new-lesson/add_section/', AddSectionPage.as_view(), name='add_section'),
    path('new-lesson/add_theme/', AddThemePage.as_view(), name='add_theme'),
    path('new-lesson/confirm/', SurePage.as_view(), name='sure'),
    path('learning-page/lesson/', LessonPage.as_view(), name='lesson_page'),
    path('learning-page/end-lesson/', EndLessonPage.as_view(), name='end_lesson'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
