from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import HomePage, GoalPage

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('goal-page/<int:goal_id>', GoalPage.as_view(), name='goal_page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
