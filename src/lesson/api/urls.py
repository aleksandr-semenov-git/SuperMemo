from django.urls import path
from django.conf import settings
from .api_views import Lessons, Sections, Themes, LessonDetails, SectionDetails, ThemeDetails

urlpatterns = [
    path('lessons/', Lessons.as_view(), name='lessons'),
    path('lesson/<int:pk>/', LessonDetails.as_view(), name='lesson_details'),

    path('sections/', Sections.as_view(), name='sections'),
    path('section/<int:pk>/', SectionDetails.as_view(), name='section_details'),

    path('themes/', Themes.as_view(), name='themes'),
    path('theme/<int:pk>/', ThemeDetails.as_view(), name='theme_details'),
]
