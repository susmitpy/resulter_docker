from .models import *

# OPTIMIZE Eng, BK, OC, ECO, PT, EVS All students

def set_up_exams():
    subjects = Subject.objects.all()
    exams = ["unit_one","terminal","unit_two","final_theory","final_oral"]
    pt_exams = ["theory","practical"]
    evs_exams = ["project","seminar"]
    a = Division.objects.all()
    divisions = [i.get("name") for i in a.all().values()]
    for division in divisions:
        for subject in subjects:
            for exam in exams:
                Exam.objects.create(name=exam,subject=subject,division=division)
        for exam in pt_exams:
            PT_EVS_Exam.objects.create(exam=exam,subject="PT",division=division)
        for exam in evs_exams:
            PT_EVS_Exam.objects.create(exam=exam,division=division,subject="EVS")

def set_up_pt_evs_assmts():
    exams = PT_EVS_Exam.objects.all()
    assessments = []
    for exam in exams:
        div = exam.division

        students = Student.objects.filter(division=div).exclude(vacant=True)
        for student in students:
             a = PT_EVS_Assessment(exam=exam,student=student)
             assessments.append(a)
    PT_EVS_Assessment.objects.bulk_create(assessments)


def set_up_assmts():
    exams = Exam.objects.all()
    assessments = []
    for exam in exams:
        div = exam.division
        sub = exam.subject
        # Optimize, this in fetching all studets again and again for num_subjects * 5 times
        students = Student.objects.filter(division=div,subjects=sub).exclude(vacant=True)
        for student in students:
             a = Assessment(exam=exam,student=student)
             assessments.append(a)
    Assessment.objects.bulk_create(assessments)

def set_up_all():
    set_up_exams()
    set_up_pt_evs_assmts()
    set_up_assmts()
