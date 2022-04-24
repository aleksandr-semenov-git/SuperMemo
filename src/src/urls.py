from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from lesson.api.api_views import APILessons

router = DefaultRouter()
router.register('new-lessons', APILessons)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('memo.urls', 'memo'), namespace='memo')),
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('lesson/', include(('lesson.urls', 'lesson'), namespace='lesson')),
    path('repeat/', include(('repeat.urls', 'repeat'), namespace='repeat')),

    path('api/', include(('memo.api.urls', 'goal_api'), namespace='goal_api')),
    path('api/', include(('account.api.urls', 'account_api'), namespace='account_api')),
    path('api/', include(('lesson.api.urls', 'lesson_api'), namespace='lesson_api')),
    path('api/', include(router.urls)),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/base-auth/', include('rest_framework.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth-token/', include('djoser.urls.authtoken')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/support/', include(('support.api.urls', 'support_api'), namespace='support_api')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

