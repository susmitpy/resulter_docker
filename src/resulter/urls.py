from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("",include("landing.urls")),
    path("management/", include("management.urls")),
    path("dashboard/",include("dashboard.urls")),
    path("public/",include("public.urls")),
    path("teacher/",include("teacher.urls")),
    path('admin/', admin.site.urls),
    path(r'^registration/', include('django.contrib.auth.urls'))
]
