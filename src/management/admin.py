from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Division)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Exam)
admin.site.register(PT_EVS_Exam)
admin.site.register(Assessment)
admin.site.register(PT_EVS_Assessment)
admin.site.register(AssessmentLog)
admin.site.register(PT_EVS_AssessmentLog)
admin.site.register(MarksheetBulkUpdateLog)
admin.site.register(SportsData)
admin.site.register(Info)
