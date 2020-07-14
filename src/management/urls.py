from django.urls import path

from . import views

from resulter import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='mngt_home'),
    path('upload_student_details',views.upload_student_details_file, name="upload_student_details"),
    path('upload_students_subjects',views.upload_students_subjects, name="upload_students_subjects"),
    path('set_up_exam_assmts',views.set_up_exam_assmts, name="set_up_exam_assmts"),
    path("view_student_details",views.view_student_details,name="view_student_details"),
    path("update_student_details",views.update_student_details,name="update_student_details"),
    path("CreateNewStudent",views.CreateNewStudent.as_view(),name="CreateNewStudent"),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
