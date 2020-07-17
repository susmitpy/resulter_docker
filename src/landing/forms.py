from django import forms

class EmailFieldForm(forms.Form):

    email = forms.EmailField()
