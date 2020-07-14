import json

from django.shortcuts import render

from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse

from .forms import FileUpload, StudentSelector, MarksEntryDivisionSubjectSelectForm

from .models import Assessment, Subject, Division, Exam, MarksheetBulkUpdateLog, Info, Student
from .exam_assmt_set_up import set_up_all

from .file_handling_interface import handle_student_details_uploaded_file, handle_students_subjects_uploaded_file, handle_marksheet_uploaded_file

import pandas as pd

from io import BytesIO
import mimetypes
from django.core.files.storage import default_storage

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from landing.decorators import allowed_users

from django.views import View


import numpy as np

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","administration"])
def upload_student_details_file(req):
    if req.method == 'POST':
        form = FileUpload(req.POST, req.FILES)
        if form.is_valid():
            handle_student_details_uploaded_file(req.FILES['file'])
            return render(req,'management/upload_student_details_success.html/')
    else:
        form = FileUpload()
    return render(req, 'management/upload_student_details.html', {'form': form})

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","administration"])
def view_student_details(req):
    if req.method == 'POST':
        form = StudentSelector(req.POST, req.FILES)
        if form.is_valid():
            division = form.cleaned_data["division"]
            roll = form.cleaned_data["roll"]
            student = Student.objects.get(division=division,roll_num=roll)

            subjects = [i["name"] for i in list(student.subjects.all().values("name"))]
            all_subjects = [i["name"] for i in list(Subject.objects.all().values("name"))]
            a = Division.objects.all()
            divisions = [i.get("name") for i in a.all().values()]
            return render(req,'management/student_details.html/',{"student":student,"subjects":subjects,"all_subjects":all_subjects,"divisions":divisions})
    else:
        form = StudentSelector()
    return render(req, 'management/student_selector.html/', {'form': form})

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","administration"])
def update_student_details(req):
    student_id = req.POST.get("id")
    field = req.POST.get("field")
    new_val = json.loads(req.POST.get("newVal"))
    print("Student ID: {}\nField: {}\nNew Value: {}".format(str(student_id),str(field),str(new_val)))

    if field != "subjects":
        Student.objects.filter(id=student_id).update(**{field:new_val})
    else:
        subs = Subject.objects.filter(name__in=new_val)
        s=Student.objects.get(pk=student_id)
        s.subjects.set(subs)
        s.save()
    return JsonResponse({"status":"success"}, status=200)

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","administration"])
def upload_student_details_file(req):
    if req.method == 'POST':
        form = FileUpload(req.POST, req.FILES)
        if form.is_valid():
            handle_student_details_uploaded_file(req.FILES['file'])
            return render(req,'management/upload_student_details_success.html/')
    else:
        form = FileUpload()
    return render(req, 'management/upload_student_details.html', {'form': form})

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","administration"])
def upload_students_subjects(req):
    if req.method == 'POST':
        form = FileUpload(req.POST, req.FILES)
        if form.is_valid():
            handle_students_subjects_uploaded_file(req.FILES['file'])
            return render(req,'management/upload_students_subjects_success.html/')
    else:
        form = FileUpload()
    return render(req, 'management/upload_students_subjects.html', {'form': form})

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","administration"])
def home(req):
    info = Info.objects.exists()
    if info:
        info = Info.objects.first()
        exams_assmts_set_up_already = info.exam_assmt_set_up_done == True
    else:
        Info.objects.create()
        exams_assmts_set_up_already = False
    print(exams_assmts_set_up_already)
    context = {
        "exam_assmt_set_up" : exams_assmts_set_up_already
    }
    return render(req, 'management/home.html',context)

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","administration"])
def set_up_exam_assmts(req):
    if req.method == "POST":
        print("Create Exam, Assessments")
        set_up_all()
        Info.objects.update(exam_assmt_set_up_done=True)
        return JsonResponse({"status":"success"}, status=200)


# DB CHECK PASS
class CreateNewStudent(View):
    def get(self,req):
        context = self.get_context()
        return render(req,"management/create_student.html",context)

    def post(self,req):
        data = json.loads(req.POST.get("data"))
        self.handle_data(data)
        return JsonResponse({"status":"Success"},status=200)

    def get_context(self):
        subjects = [i["name"] for i in list(Subject.objects.all().values("name"))]
        a = Division.objects.all()
        divisions = [i.get("name") for i in a.all().values()]
        return {"subjects":subjects,"divisions":divisions}

    def handle_data(self,data):
        name = data["name"]
        division = data["division"]
        roll_num = data["roll_num"]
        identifier = data["identifier"]
        subjects = data["subjects"]

        s = Student.objects.create(name=name,division=division,roll_num=roll_num,identifier=identifier)
        subs_objs = Subject.objects.filter(name__in=subjects)
        s.subjects.set(subs_objs)

        s.save()
