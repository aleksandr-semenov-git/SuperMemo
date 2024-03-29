from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import LoginView, RegistrationView, LogoutView, ProfilePage, EditPage, ProfilePageBasic, AddGoalPage

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             success_url='/account/password-reset/done/'),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url='/account/reset/done/'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html',
         ),
         name='password_reset_complete'),

    path('profile/', ProfilePageBasic.as_view(), name='profile_basic'),
    path('profile/<str:username>', ProfilePage.as_view(), name='profile'),
    path('profile/edit/', EditPage.as_view(), name='profile_edit'),

    path('profile/edit/password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='registration/password_change_form.html',
             success_url='/profile/edit/password_change_done'),
         name='password_change'),

    path('profile/edit/password_change_done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('add-goal/', AddGoalPage.as_view(), name='add_goal'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
