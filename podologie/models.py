from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)    
    
    def __str__(self):
        return self.user.username

class Service(models.Model):  
    Duration_LIST = (
        (0, '15 min'),
        (1, '30 min'),
        (2, '45 min'),
        (3, '60 min'),
    ) 
    motif = models.CharField(max_length=150, name="motif")
    duration = models.IntegerField(blank=False, choices=Duration_LIST)
    
    def __str__(self):
        return '{} ({}) '.format(self.motif, self.timing)      

    @property
    def timing(self):
        return self.Duration_LIST[self.duration][1]
    
    
class Appointment(models.Model): 

    date = models.DateField(name='date')
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank= True)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    motif = models.ForeignKey(Service, on_delete=models.CASCADE) 
    booked_date = models.DateTimeField(auto_now_add=True) 
    precisions = models.CharField(blank=True, null=True, max_length=240) 

    def __str__(self):
        return '{}. Patient: {}'.format(self.start_time, self.patient)  


class ClosedDate(models.Model):
    """
    Simple model to store unavailable dates
    """
    date = models.DateField()
    
    def __str__(self):
        return '{}'.format(self.date)
    
    def serialize(self):
        return {'date': self.date}