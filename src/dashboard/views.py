from django.shortcuts import render, redirect
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd

from management.models import Assessment, Division, Student,AssessmentLog, MarksheetBulkUpdateLog,PT_EVS_AssessmentLog

from django.db.models import Avg

from .result_generator import generate_intermediate_result

from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.decorators import login_required

import re

from landing.decorators import allowed_users


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def home(req):
    return render(req,"dashboard/home.html")

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def marksheet_bulk_update_log(req):
    log=MarksheetBulkUpdateLog.objects.values("exam","division","subject","updated_by","updated_at")
    if log.exists():
        df=pd.DataFrame(log)
        df.columns = ["Exam","Division","Subject","User","Timestamp"]
        df["Timestamp"]  = pd.to_datetime(df["Timestamp"])
        df["Timestamp"] = df["Timestamp"].dt.tz_convert("Asia/Kolkata").dt.strftime("%d/%m/%y %H:%M")

        df["Name"] = df["User"].map(lambda x: User.objects.get(email=x).get_full_name())
        df["User"] = df["Name"] + "\n" + df["User"]
        df = df.drop("Name",axis=1)

        df = df.sort_values("Timestamp",ascending=False)

        df = df.to_html(classes=["mystyle table table-bordered table-striped"],index=False,table_id="mytable")
        df = re.sub('<tbody>', '<tbody id="log">',df)

        replace = """
            <thead>
                <tr class="filters" style="text-align: right;">
                    <th><input type="text" class="form-control" placeholder="Exam" disabled></th>
                    <th><input type="text" class="form-control" placeholder="Division" disabled></th>
                    <th><input type="text" class="form-control" placeholder="Subject" disabled></th>
                    <th><input type="text" class="form-control" placeholder="User" disabled></th>
                    <th><input type="text" class="form-control" placeholder="Timestamp" disabled></th>
                </tr>
            </thead>
        """

        df = re.sub(r"<thead>.+<\/thead>",replace,df,flags=re.S)
        df = df.replace("\\n","<br>")
    else:
        df = pd.DataFrame()

    return render(req,"dashboard/marksheet_bulk_update_log.html",{"df":df})

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def graded_assessment_log(req):
    log= PT_EVS_AssessmentLog.objects.values("assmt__exam__exam","assmt__exam__subject","assmt__student__division","assmt__student__roll_num","old_marks","new_marks","updated_by","updated_at")
    print(log.exists())
    if log.exists():

        df = pd.DataFrame(log)
        exam_name_mapping = {'theory': 'Theory',
             'practical': 'Practical',
             "project" : "Project",
             "seminar" : "Seminar"}

        df.columns = ["Exam","Subject","Division","Roll","Old Marks","New Marks","User","Timestamp"]
        df["Exam"] = df["Exam"].map(exam_name_mapping)
        df["Timestamp"]  = pd.to_datetime(df["Timestamp"])
        df["Timestamp"] = df["Timestamp"].dt.tz_convert("Asia/Kolkata").dt.strftime("%d/%m/%y %H:%M")

        df["Name"] = df["User"].map(lambda x: User.objects.get(email=x).get_full_name())
        df["User"] = df["Name"] + "\n" + df["User"]
        df = df.drop("Name",axis=1)

        df = df.sort_values("Timestamp",ascending=False)

        df = df.to_html(classes=["mystyle table table-bordered table-striped"],index=False,table_id="mytable")
        df = re.sub('<tbody>', '<tbody id="log">',df)

        replace = """
            <thead>
                <tr class="filters" style="text-align: right;">
                    <th><input type="text" class="form-control" placeholder="Exam" disabled></th>
                    <th><input type="text" class="form-control" placeholder="Subject" disabled></th>
                    <th><input type="text" class="form-control" placeholder="Division" disabled></th>
                    <th><input type="text" class="form-control" placeholder="Roll" disabled></th>
                    <th><input type="text" class="form-control" placeholder="Old Marks" disabled></th>
                    <th><input type="text" class="form-control" placeholder="New Marks" disabled></th>
                    <th><input type="text" class="form-control" placeholder="User" disabled></th>
                    <th><input type="text" class="form-control" placeholder="Timestamp" disabled></th>

                </tr>
            </thead>
        """

        df = re.sub(r"<thead>.+<\/thead>",replace,df,flags=re.S)
        df = df.replace("\\n","<br>")
    else:
        df = pd.DataFrame()

    return render(req,"dashboard/assessment_log.html",{"df":df})

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def assessment_log(req):
    log= AssessmentLog.objects.values("assmt__exam__name","assmt__exam__subject__name","assmt__student__division","assmt__student__roll_num","old_marks","new_marks","updated_by","updated_at")
    print(log.exists())
    if log.exists():

        df = pd.DataFrame(log)
        name_mapping = {'unit_one': '1st Unit Test',
        'terminal': 'Terminal Examination',
        'unit_two': '2nd Unit Test',
        'final_theory': 'Final Examination Theory',
        'final_oral': 'Final Examination Practical / Oral'}

        df.columns = ["Exam","Subject","Division","Roll","Old Marks","New Marks","User","Timestamp"]
        df["Exam"] = df["Exam"].map(name_mapping)
        df["Timestamp"]  = pd.to_datetime(df["Timestamp"])
        df["Timestamp"] = df["Timestamp"].dt.tz_convert("Asia/Kolkata").dt.strftime("%d/%m/%y %H:%M")

        df["Name"] = df["User"].map(lambda x: User.objects.get(email=x).get_full_name())
        df["User"] = df["Name"] + "\n" + df["User"]
        df = df.drop("Name",axis=1)

        df = df.sort_values("Timestamp",ascending=False)

        df = df.to_html(classes=["mystyle table table-bordered table-striped"],index=False,table_id="mytable")
        df = re.sub('<tbody>', '<tbody id="log">',df)

        replace = """
            <thead>
                <tr class="filters" style="text-align: right;">
                    <th><input type="text" class="form-control" placeholder="Exam" disabled></th>
                    <th><input type="text" class="form-control" placeholder="Subject" disabled></th>
                    <th><input type="text" class="form-control" placeholder="Division" disabled></th>
                    <th><input type="text" class="form-control" placeholder="Roll" disabled></th>
                    <th><input type="text" class="form-control" placeholder="Old Marks" disabled></th>
                    <th><input type="text" class="form-control" placeholder="New Marks" disabled></th>
                    <th><input type="text" class="form-control" placeholder="User" disabled></th>
                    <th><input type="text" class="form-control" placeholder="Timestamp" disabled></th>

                </tr>
            </thead>
        """

        df = re.sub(r"<thead>.+<\/thead>",replace,df,flags=re.S)
        df = df.replace("\\n","<br>")
    else:
        df = pd.DataFrame()

    return render(req,"dashboard/assessment_log.html",{"df":df})

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def assessments_with_notes(req):
    assmts = []
    assessments_with_notes=Assessment.objects.exclude(note__in=["ABSENT",""]).values("student__identifier","exam__name","exam__subject__name","exam__division","student__roll_num","marks","note").all()
    if assessments_with_notes.exists():
        df = pd.DataFrame(assessments_with_notes)
        name_mapping = {'unit_one': '1st Unit Test',
        'terminal': 'Terminal Examination',
        'unit_two': '2nd Unit Test',
        'final_theory': 'Final Examination Theory',
        'final_oral': 'Final Examination Practical / Oral'}
        df.columns = ["Identifier","Exam","Subject","Division","Roll","Marks","Note"]
        df["Exam"] = df["Exam"].map(name_mapping)

        df = df.to_html(classes=["mystyle table table-bordered table-striped"],index=False,table_id="mytable")
    else:
        df = pd.DataFrame()

    return render(req, "dashboard/assessments_with_notes.html",{"df":df})

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def subject_exam_division_plots(req):
    a=Assessment.objects.exclude(marks=-1).values("exam__name","exam__division","exam__subject__name").annotate(Avg("marks"))
    df = pd.DataFrame(a)
    df = df.dropna()
    name_mapping = {'unit_one': 'Unit 1',
 'terminal': 'Terminal',
 'unit_two': 'Unit 2',
 'final_theory': 'Final',
 'final_oral': 'Oral'}
    df["exam__name"] = df["exam__name"].map(name_mapping)
    plots = []
    for div in list(df["exam__division"].unique()):
        div_data = df[df["exam__division"]==div]
        config = dict({'displayModeBar': False})
        fig = go.Figure()

        sz = [10,20,30,40]
        fig.add_trace(go.Scatter(
            x=div_data["exam__name"],
            y=div_data["exam__subject__name"],
            text = div_data["marks__avg"].round(),

            mode="markers+text",
            marker=go.scatter.Marker(
                size=div_data["marks__avg"],
                opacity=0.4,
                line=dict(width=2,color='#0F0F0F'),

            ),

        ))

        fig.update_layout(title="Division: {}".format(div),xaxis_title="Exams",yaxis_title="Subjects", font=dict(
        family="Courier New, monospace",
        size=14,
        color="#7f7f7f"
    ))

        plt_div = plot(fig, output_type='div',config=config)
        data = {"plot":plt_div}
        plots.append(data)
    return render(req, "dashboard/subject_exam_division_plots.html", context={'data': plots})

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def intermediate_result(req):
    if req.method == 'POST':
            division = req.POST.get("division")
            ff = req.POST.get("format")

            print("File Format: " + ff)
            file_path = generate_intermediate_result(division)
            return JsonResponse({"filePath":file_path}, status=200)

    a = Division.objects.all()
    divisions = [i.get("name") for i in a.all().values()]
    return render(req,"dashboard/intermediate_result.html",{"divisions":divisions})

# DB CHECK PASS
def get_student_info(ID):
     s = Student.objects.get(pk=ID)
     return s.info

# DB CHECK PASS
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin","faculty"])
def student_performance(req):
     students = Student.objects.exclude(vacant=True).values("id","assessment__exam__subject__name").annotate(Avg("assessment__marks"))

     df = pd.DataFrame(students)
     df.columns = ["id","Subject","Marks"]
     df["Marks"] = df["Marks"].replace({-1:None})
     df = df.dropna()
     if len(df) == 0:
         return render(req,"dashboard/student_performance.html",{"show":False})
     avg=df.groupby("id")["Marks"].mean()
     df=df.join(avg,on="id",rsuffix="_avg")
     df["diff"] = (df["Marks"]-df["Marks_avg"]).abs()
     alert=df[(df["diff"]>2) & (df["Marks"] < df["Marks_avg"])]
     alert["student"]=alert["id"].map(get_student_info)
     alert[["Division","Roll","Name"]] = alert["student"].str.split(",",expand=True)
     alert.drop(["student","diff","id"],inplace=True,axis=1)
     alert.rename({"Marks_avg":"Avg Marks"},axis=1,inplace=True)
     alert = alert.to_html(classes=["mystyle table table-bordered table-striped"],index=False)
     return render(req,"dashboard/student_performance.html",{"alert":alert,"show":True})
