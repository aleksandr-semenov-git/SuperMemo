from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include(('lesson.urls', 'lesson'), namespace='lesson')),
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('', include(('memo.urls', 'memo'), namespace='memo')),

    path('api/', include(('account.api.urls', 'lesson_api'), namespace='lesson_api')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
