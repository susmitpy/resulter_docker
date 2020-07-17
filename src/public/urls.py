from django.urls import path

from . import views

from resulter import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='public_home'),
    path("fy_result",views.fy_result,name="fy_result")
    ]


urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
