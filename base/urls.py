from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls', namespace='common')),
    path('', include('advert.urls', namespace='advert')),
]


if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
