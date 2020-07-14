from django.urls import path

from . import views

from resulter import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='teacher_home'),
    path("sports",views.sports,name="sports"),
    path("insert_sports_data",views.insert_sports_data,name="insert_sports_data"),
    path("update_sports_data",views.update_sports_data,name="update_sports_data"),
    path("delete_sports_data",views.delete_sports_data,name="delete_sports_data"),
    path("marksheet",views.marksheet,name="marksheet"),
    path('upload_marksheet',views.upload_marksheet, name="upload_marksheet"),
    path("download_marksheet",views.download_marksheet,name="download_marksheet"),
    path('update_assmt',views.update_assmt, name="update_assmt"),
    path("submit_assmts",views.submit_assmts,name="submit_assmts"),
    path("GradedMarksheet",views.GradedMarksheet.as_view(),name="GradedMarksheet"),
    path('graded_upload_marksheet',views.graded_upload_marksheet, name="graded_upload_marksheet"),
    path('graded_update_assmt',views.graded_update_assmt, name="graded_update_assmt"),
    path("graded_submit_assmts",views.graded_submit_assmts,name="graded_submit_assmts"),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
