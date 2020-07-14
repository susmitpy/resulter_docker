from django.db import models

from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

from django.utils import timezone

from django.db.utils import OperationalError


class Division(models.Model):
    name = models.CharField(max_length = 5, default="")

    def __str__(self):
        return self.name

division_list = [('', '')]
try:
    division_list.extend([(i[0],i[0])
        for i in Division.objects.values_list('name')])
except OperationalError:
    pass  # happens when db doesn't exist yet, views.py should be
          # importable without this side effect

class Subject(models.Model):
    name = models.CharField(max_length = 30, default="")

    def __str__(self):
        return self.name

class Student(models.Model):
    roll_num = models.IntegerField()
    name = models.CharField(max_length = 30, default="")
    division = models.CharField(max_length=5,choices=division_list,null=True, default="")
    subjects = models.ManyToManyField(Subject)
    identifier = models.CharField(max_length=8,help_text="LD / Specify ",default="",blank=True)
    sports = models.IntegerField(default=0)
    vacant = models.BooleanField(default=False)

    class Meta:
        constraints = [
         models.UniqueConstraint(fields=['roll_num', 'division'], name='unique_student')
        ]

    def __str__(self):
        return str(self.roll_num) + " " + self.name

    @property
    def info(self):
        return ''.join(
            [self.division,' ,', str(self.roll_num), ' ,', self.name])

class Exam(models.Model):
    name_mapping = {'unit_one': '1st Unit Test',
 'terminal': 'Terminal Examination',
 'unit_two': '2nd Unit Test',
 'final_theory': 'Final Examination Theory',
 'final_oral': 'Final Examination Practical_Oral'}
    choices = [(i,j) for i,j in name_mapping.items()]
    name = models.CharField(max_length=20,choices = choices, default="")
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    division = models.CharField(max_length=5,choices=division_list,null=True, default="")

    def __str__(self):
        subject_name = Subject.objects.get(id=self.subject.id).name
        return self.name_mapping[self.name] + " " + subject_name + " Division: " + self.division

class PT_EVS_Exam(models.Model):
    exam_name_mapping = {'theory': 'Theory',
 'practical': 'Practical',
 "project" : "Project",
 "seminar" : "Seminar"}
    choices = [(i,j) for i,j in exam_name_mapping.items()]
    exam = models.CharField(max_length=20,choices = choices, default="")
    choices = [("PT","Physcial Education"),("EVS","Environmental Science")]
    subject = models.CharField(max_length=5,choices=choices)
    division = models.CharField(max_length=5,choices=division_list,null=True)

    def __str__(self):
        return self.subject + " " + self.exam_name_mapping[self.exam] + " "  + " Division: " + self.division

class AbstractAssessment(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    marks = models.IntegerField(null=True,blank=True)
    note = models.CharField(max_length=8,help_text="ABSENT / COPY CASE / BLANK / specify",blank=True)

    class Meta:
       abstract = True

class Assessment(AbstractAssessment):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)

class PT_EVS_Assessment(AbstractAssessment):
    exam = models.ForeignKey(PT_EVS_Exam,on_delete=models.CASCADE)

class AbstractAssessmentLog(models.Model):
    old_marks = models.IntegerField(null=True)
    new_marks = models.IntegerField(null=True)
    updated_at = models.DateTimeField(default=timezone.localtime)
    updated_by = models.CharField(max_length=20,default="ADMIN")

    class Meta:
       abstract = True

class AssessmentLog(AbstractAssessmentLog):
    assmt = models.ForeignKey(Assessment,on_delete=models.CASCADE,null=True)

class PT_EVS_AssessmentLog(AbstractAssessmentLog):
    assmt = models.ForeignKey(PT_EVS_Assessment,on_delete=models.CASCADE)

class MarksheetBulkUpdateLog(models.Model):
    exam = models.CharField(max_length=40)
    division = models.CharField(max_length=40)
    subject = models.CharField(max_length=40)
    updated_at = models.DateTimeField(default=timezone.localtime)   # Inspect
    updated_by = models.CharField(max_length=20,default="ADMIN")

    def __str__(self):
        return " ".join([self.exam,self.subject,self.division])

class SportsData(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    sport = models.CharField(max_length=20,blank=True)
    stage = models.CharField(max_length=20,blank=True)
    extra_marks = models.IntegerField(default=0)

    def __str__(self):
        return " ".join(["Stage:", self.stage, "Marks: ",str(self.extra_marks)])

class Info(models.Model):
    exam_assmt_set_up_done = models.BooleanField(default=False)
