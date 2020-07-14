from django.urls import path

from . import views

from resulter import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path("fy_result",views.fy_result,name="fy_result")
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
