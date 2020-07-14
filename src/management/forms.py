#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 10:35:44 2020

@author: susmitvengurlekar
"""

from django import forms

from .models import Division, Subject
from django.db.utils import OperationalError

division_list = [('', '')]
subject_list = [('', '')]

try:
    division_list.extend([(i[0],i[0])
        for i in Division.objects.values_list('name')])
    subject_list.extend([(i[0],i[0])
        for i in Subject.objects.values_list('name')])
except OperationalError:
    pass  # happens when db doesn't exist yet, views.py should be
          # importable without this side effect

class FileUpload(forms.Form):
    file = forms.FileField()


class StudentSelector(forms.Form):
    """
    Select Student for getting details
    """

    division = forms.ChoiceField(choices=division_list)
    roll = forms.IntegerField()

class MarksEntryDivisionSubjectSelectForm(forms.Form):
    division = forms.ChoiceField(choices=division_list)

    subject = forms.ChoiceField(choices=subject_list)
    choices = [('unit_one', '1st Unit Test'), ('terminal', 'Terminal Examination'), ('unit_two', '2nd Unit Test'), ('final_theory', 'Final Examination Theory'), ('final_oral', 'Final Examination Practical / Oral')]
    exam = forms.ChoiceField(choices=choices)
