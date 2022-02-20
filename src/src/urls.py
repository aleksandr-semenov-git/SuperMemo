from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

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

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

