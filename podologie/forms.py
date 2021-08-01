from django import forms
from datetime import date



from django.forms.widgets import DateInput


from .models import Service, Appointment

class PatientForm(forms.Form):
    name = forms.CharField(label="Nom ", max_length=64)
    firstname = forms.CharField(label="Prénom ", max_length=64)
    email = forms.EmailField(label="Mail ", max_length=128)

class VisitForm(forms.Form):
    motif = forms.ModelChoiceField(queryset=Service.objects.all(), initial= 0, label="Choix motifs")


    



