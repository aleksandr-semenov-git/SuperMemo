from django.urls import path
from .views import HomePage, GoalPage, AddGoalPage, MyGoalsPage
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('add-goal/', AddGoalPage.as_view(), name='add_goal'),
    path('choose-goal/', MyGoalsPage.as_view(), name='choose_goal'),
    path('my-goals/', MyGoalsPage.as_view(), name='my_goals'),
    path('my-goals/goal-page/<int:goal_id>', GoalPage.as_view(), name='goal_page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
