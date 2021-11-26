from django.urls import path
from .views import HomePage, GoalPage, AddGoalPage
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('profile/add-goal/', AddGoalPage.as_view(), name='add_goal'),
    path('goal-page/<int:goal_id>', GoalPage.as_view(), name='goal_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
