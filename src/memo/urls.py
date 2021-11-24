from django.urls import path
from .views import HomePage, ProfilePage, EditPage, ProfilePageBasic, GoalPage, AddGoalPage
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('profile/', ProfilePageBasic.as_view(), name='profile_basic'),
    path('profile/<str:username>', ProfilePage.as_view(), name='profile'),
    path('profile/edit/', EditPage.as_view(), name='edit'),
    path('profile/add-goal/', AddGoalPage.as_view(), name='add_goal'),
    path('goal-page/<int:goal_id>', GoalPage.as_view(), name='goal_page'),

    path('profile/edit/password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='registration/password_change_form.html',
             success_url='/profile/edit/password_change_done'),
         name='password_change'),

    path('profile/edit/password_change_done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'),
         name='password_change_done'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
