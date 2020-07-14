#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 10:42:27 2020

@author: susmitvengurlekar
"""
import pandas as pd
from management.models import Student, Subject,Exam,Assessment,MarksheetBulkUpdateLog, PT_EVS_Exam, PT_EVS_Assessment

def get_note(x):
    x = str(x)
    if x == "":
        return "BLANK"
    elif x.startswith("0"):
        return "ZERO"
    elif x.upper().startswith("C"):
        return "COPY CASE"
    elif x.upper().startswith("A"):
        return "ABSENT"
    return ""

def graded_handle_marksheet_uploaded_file(f,exam_id,username):
    e = PT_EVS_Exam.objects.get(pk=exam_id)
    assmts = e.pt_evs_assessment_set.all()
    ids, rolls = [],[]
    for assmt in assmts:
        ids.append(assmt.id)
        rolls.append(assmt.student.roll_num)
    ass_info = pd.DataFrame({"ID":ids,"roll":rolls})


    df = pd.read_excel(f)
    df.fillna("",inplace=True)
    df["note"] = df["marks"].apply(get_note)


    df["marks"] = pd.to_numeric(df["marks"],errors="coerce")
    df["marks"].fillna(-1,inplace=True)

    df = df.merge(ass_info,on="roll")

    assessments = []
    for index, row in df.iterrows():
        ID = row["ID"]
        marks = row["marks"]
        note = row["note"]
        a = PT_EVS_Assessment(id=ID,marks=marks,note=note)
        assessments.append(a)


    PT_EVS_Assessment.objects.bulk_update(assessments,["marks","note"])
    MarksheetBulkUpdateLog.objects.create(exam=e.exam_name_mapping.get(e.exam),division=e.division,subject=e.subject,updated_by=username)


# DB CHECK PASS
def handle_marksheet_uploaded_file(f,exam_id,username):
    e = Exam.objects.get(pk=exam_id)
    assmts = e.assessment_set.all()
    ids, rolls = [],[]
    for assmt in assmts:
        ids.append(assmt.id)
        rolls.append(assmt.student.roll_num)
    ass_info = pd.DataFrame({"ID":ids,"roll":rolls})


    df = pd.read_excel(f)
    df.fillna("",inplace=True)
    df["note"] = df["marks"].apply(get_note)


    df["marks"] = pd.to_numeric(df["marks"],errors="coerce")
    df["marks"].fillna(-1,inplace=True)

    df = df.merge(ass_info,on="roll")

    assessments = []
    for index, row in df.iterrows():
        ID = row["ID"]
        marks = row["marks"]
        note = row["note"]
        a = Assessment(id=ID,marks=marks,note=note)
        assessments.append(a)


    Assessment.objects.bulk_update(assessments,["marks","note"])
    MarksheetBulkUpdateLog.objects.create(exam=e.name_mapping.get(e.name),division=e.division,subject=e.subject__name,updated_by=username)
