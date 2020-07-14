from django.urls import path

from . import views

from resulter import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='dashboard_home'),
    path("subject_exam_division_plots",views.subject_exam_division_plots,name="subject_exam_division_plots"),
    path("assessments_with_notes",views.assessments_with_notes,name="assessments_with_notes"),
    path("intermediate_result",views.intermediate_result,name="intermediate_result"),
    path("student_performance",views.student_performance,name="student_performance"),
    path("assessment_log",views.assessment_log,name="assessment_log"),
    path("marksheet_bulk_update_log",views.marksheet_bulk_update_log,name="marksheet_bulk_update_log"),
    path("graded_assessment_log",views.graded_assessment_log,name="graded_assessment_log")
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
