import json

from django.shortcuts import render

from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse

from .forms import FileUpload, MarksEntryDivisionSubjectSelectForm

from management.models import Assessment, Subject, Division, Exam,PT_EVS_Exam, MarksheetBulkUpdateLog, SportsData, PT_EVS_Assessment, PT_EVS_AssessmentLog

from .file_handling_interface import handle_marksheet_uploaded_file,graded_handle_marksheet_uploaded_file

import pandas as pd

from io import BytesIO
import mimetypes
from django.core.files.storage import default_storage

from management.models import Student, AssessmentLog
from django.views import View
from django.utils.decorators import method_decorator

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from landing.decorators import allowed_users
import numpy as np

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def update_assmt(req):
    if req.method == "POST":
        print("Update Assessment")
        marks = req.POST.get("marks")
        note = req.POST.get("note")
        assmt_id = req.POST.get("assmt_id")
        assmt = Assessment.objects.get(id=assmt_id)
        old_marks=assmt.marks
        assmt.marks = marks
        assmt.note = note
        assmt.save()
        if old_marks != marks:
            print(req.user)
            log = AssessmentLog(assmt=assmt,old_marks=old_marks,new_marks=marks,updated_by=req.user.email)
            log.save()
        return JsonResponse({"status":"success"},status=200)

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def submit_assmts(req):
    if req.method == "POST":
        print("Update Assessment")
        assmts = json.loads(req.POST.get("assmts"))

        assmts_objs = [Assessment(id=a["id"],marks=a["marks"],note=a["note"]) for a in assmts]
        Assessment.objects.bulk_update(assmts_objs,["marks","note"])

        exam = req.POST.get("exam")
        subject = req.POST.get("subject")
        division = req.POST.get("division")

        print((exam,subject,division))

        MarksheetBulkUpdateLog.objects.create(exam=exam,division=division,subject=subject,updated_by=req.user.email)

        return JsonResponse({"status":"success"},status=200)

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def upload_marksheet(req):
    if req.method == "POST":
        print("Upload Marksheet")
        form = FileUpload(req.POST, req.FILES)
        file = req.FILES['file']
        if form.is_valid():
            file = req.FILES['file']
            exam_id = req.POST.get("exam_id")
            handle_marksheet_uploaded_file(file,exam_id,req.user.usename)
            print("Exam ID: " + str(exam_id))
            return render(req,"teacher/upload_marksheet_success.html")

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def download_marksheet(req):
    if req.method == "POST":
        print("Download marksheet")
        assmts = json.loads(req.POST.get("assmts"))
        division = req.POST.get("division")
        subject = req.POST.get("subject")
        exam = req.POST.get("exam")
        df = pd.DataFrame(assmts)
        df["marks"] = np.where(df["marks"]=="-1",df["note"],df["marks"])
        df=df.drop(["note"],axis=1)

        in_memory_fp = BytesIO()


        df.to_excel(in_memory_fp,index=False)
        in_memory_fp.seek(0,0)
        file = in_memory_fp
        file_path = f"./marksheets/{exam}/{division}/{subject}.xlsx"
        default_storage.delete(file_path)
        file_name = default_storage.save(file_path, file)

        return JsonResponse({"filePath":file_path}, status=200)

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def marksheet(req):
    name_mapping = {'unit_one': '1st Unit Test',
 'terminal': 'Terminal Examination',
 'unit_two': '2nd Unit Test',
 'final_theory': 'Final Examination Theory',
 'final_oral': 'Final Examination Practical / Oral'}
    if req.method == 'POST':
        form = MarksEntryDivisionSubjectSelectForm(req.POST)
        if form.is_valid():
            division = form.cleaned_data["division"]
            subject_name = form.cleaned_data["subject"]
            exam_name = form.cleaned_data["exam"]

            subject = Subject.objects.get(name=subject_name)
            exam = Exam.objects.get(division=division,subject=subject,name=exam_name)
            assessments = Assessment.objects.filter(exam=exam)

            not_filled_marks_count = assessments.filter(marks=None).count()
            total_assmts = len(assessments)

            if not_filled_marks_count >= total_assmts/4:
                update_all_disabled = False
            else:
                update_all_disabled = True



            assmts = []
            for assmt in assessments:
                student = assmt.student
                if student.vacant:
                    continue
                asmt = {"id":assmt.id,
                        "roll":student.roll_num,
                        "identifier":student.identifier,
                        "marks":assmt.marks,
                        "note":assmt.note
                        }
                assmts.append(asmt)

            form = FileUpload()

            context = {
                    "division" : division,
                    "subject_name" : subject_name,
                    "exam_name" : name_mapping.get(exam_name),
                    "exam_id": exam.id,
                    "assessments" : assmts,
                    "form":form,
                    "update_all_disabled":update_all_disabled
                    }
            return render(req,'teacher/marks_sheet.html/',context)
    else:
        form = MarksEntryDivisionSubjectSelectForm()
    return render(req, 'teacher/marks_sheet_div_sub_exam_selector.html', {'form': form})

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def home(req):
    return render(req, 'teacher/home.html')

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def sports(req):
    data = list(SportsData.objects.values("id","student__division","student__roll_num","sport","stage","extra_marks"))
    rows = []
    for d in data:
        row = {}
        row["id"] = d["id"]
        row["division"] = d["student__division"]
        row["roll"] = d["student__roll_num"]
        row["sport"] = d["sport"]
        row["stage"] = d["stage"]
        row["marks"] = d["extra_marks"]

        rows.append(row)

    return render(req,"teacher/sports.html",{"rows":rows,"divisions":["E","F"]})

# DB CHECK PASS
def insert_sports_data(req):
    sd_id = req.POST.get("id")
    div = req.POST.get("div")
    roll = req.POST.get("roll")
    marks = req.POST.get("marks")
    stage = req.POST.get("stage")
    sport = req.POST.get("sport")

    s = Student.objects.get(division=div,roll_num=int(roll))
    s.sports = s.sports+1
    s.save()

    SportsData.objects.create(id=sd_id,sport=sport,stage=stage,extra_marks=marks,student=s)

    return JsonResponse({"status":"Success"},status=200)

# DB CHECK PASS
def update_sports_data(req):
     sd_id = req.POST.get("id")
     marks = req.POST.get("marks")
     stage = req.POST.get("stage")
     sport = req.POST.get("sport")

     SportsData.objects.filter(id=sd_id).update(extra_marks=marks,stage=stage,sport=sport)

     return JsonResponse({"status":"Success"},status=200)

# DB CHECK PASS
def delete_sports_data(req):
    sd_id = req.POST.get("id")
    sd = SportsData.objects.get(id=sd_id)
    s = sd.student
    s.sports = s.sports-1
    s.save()
    sd.delete()
    return JsonResponse({"status":"Success"},status=200)


# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def graded_update_assmt(req):
 if req.method == "POST":
     print("Update Assessment")
     marks = req.POST.get("marks")
     note = req.POST.get("note")
     assmt_id = req.POST.get("assmt_id")
     assmt = PT_EVS_Assessment.objects.get(id=assmt_id)
     old_marks=assmt.marks
     assmt.marks = marks
     assmt.note = note
     assmt.save()
     if old_marks != marks:
         print(req.user)
         log = PT_EVS_AssessmentLog(assmt=assmt,old_marks=old_marks,new_marks=marks,updated_by=req.user.email)
         log.save()
     return JsonResponse({"status":"success"},status=200)

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def graded_submit_assmts(req):
 if req.method == "POST":
     print("Update Assessment")
     assmts = json.loads(req.POST.get("assmts"))

     assmts_objs = [PT_EVS_Assessment(id=a["id"],marks=a["marks"],note=a["note"]) for a in assmts]
     PT_EVS_Assessment.objects.bulk_update(assmts_objs,["marks","note"])

     exam = req.POST.get("exam")
     subject = req.POST.get("subject")
     division = req.POST.get("division")

     print((exam,subject,division))

     MarksheetBulkUpdateLog.objects.create(exam=exam,division=division,subject=subject,updated_by=req.user.email)

     return JsonResponse({"status":"success"},status=200)

# PENDING
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def graded_upload_marksheet(req):
 if req.method == "POST":
     print("Upload Marksheet")
     form = FileUpload(req.POST, req.FILES)
     file = req.FILES['file']
     if form.is_valid():
         file = req.FILES['file']
         exam_id = req.POST.get("exam_id")
         graded_handle_marksheet_uploaded_file(file,exam_id,req.user.email)
         print("Exam ID: " + str(exam_id))
         return render(req,"teacher/upload_marksheet_success.html")

@method_decorator(login_required(login_url="login_page"), name='dispatch')
@method_decorator(allowed_users(allowed_roles=["admin","faculty"]),name="dispatch")
class GradedMarksheet(View):

    def get_exams(self):
        return {'theory': 'Theory',
     'practical': 'Practical',
     "project" : "Project",
     "seminar" : "Seminar"}

    def get(self,req):
        context = self.get_context()
        return render(req,"teacher/graded_marks_sheet_div_sub_exam_selector.html",context)

    def post(self,req):
        division = req.POST.get("division")
        subject = req.POST.get("subject")
        exam_name = req.POST.get("exam")

        print(division)
        print(subject)
        print(exam_name)

        exam = PT_EVS_Exam.objects.get(division=division,subject=subject,exam=exam_name)
        assessments = PT_EVS_Assessment.objects.filter(exam=exam)

        not_filled_marks_count = assessments.filter(marks=None).count()
        total_assmts = len(assessments)

        if not_filled_marks_count >= total_assmts/4:
            update_all_disabled = False
        else:
            update_all_disabled = True

        assmts = []
        for assmt in assessments:
            student = assmt.student
            if student.vacant:
                continue
            asmt = {"id":assmt.id,
                    "roll":student.roll_num,
                    "identifier":student.identifier,
                    "marks":assmt.marks,
                    "note":assmt.note
                    }
            assmts.append(asmt)

        form = FileUpload()

        context = {
                "division" : division,
                "subject_name" : subject,
                "exam_name" : exam_name,
                "exam_id": exam.id,
                "assessments" : assmts,
                "form":form,
                "update_all_disabled":update_all_disabled
                }
        return render(req,'teacher/graded_marks_sheet.html/',context)


    def get_context(self):
        a = Division.objects.all()
        divisions = [i.get("name") for i in a.all().values()]

        return {"divisions":divisions}
