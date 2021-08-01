from django.contrib import admin

from .models import Appointment, ClosedDate, Service, Patient, User


admin.site.register(Service)
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(ClosedDate)

