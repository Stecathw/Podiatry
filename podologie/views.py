import datetime
from pandas._libs.tslibs.timestamps import Timestamp
import pytz
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
import pandas as pd 

from .slots import day_hours, day_pause, get_slots

from .models import Appointment, Service, User, Patient, ClosedDate


START_TIME = 9
END_TIME = 17
PAUSE_START_TIME = 12
PAUSE_END_TIME = 13
APPOINTMENTS_PER_PAGE = 5


def index(request):
    return render(request, "podologie/index.html")

def rdv(request):
    return render(request, "podologie/rdv.html", { 
        "services": Service.objects.all()
    })
    
def get_unavailability(request):
    """
    API endpoint to get "disabled dates"
    """
    if request.method == "GET": 
        # Asking DB for closed days:
        dates = ClosedDate.objects.all()
        list=[]
        print(dates)
        if dates.exists():
            list = [date.date.strftime('%d-%m-%Y') for date in dates]
            print(list)     
        return JsonResponse({'dates' : list}, status=200)
    return JsonResponse({'message':'Something went wrong'}, status=400)

@login_required
def close_dates(request):
    """
    API endpoint to create "disabled dates" where no appointments could be taken
    """    
    if request.method == "POST":
        data = json.loads(request.body)
        start_date = data.get('start')
        end_date = data.get('end')
        # print(start_date, end_date) 
        # # 02-08-2021 06-08-2021 => 2021-08-02 2021-08-06        
        index = pd.date_range(start_date, end_date)     
        try :
            # Create closed days objects
            for dt in index:
                close_dt = ClosedDate.objects.create(date = dt.replace(tzinfo=pytz.UTC))
                close_dt.save()
        except IntegrityError as e:
            print(e)
            return JsonResponse({'message':'Something went wrong'}, status=400)
        return JsonResponse({}, status=200)
    return JsonResponse({'message':'Something went wrong'}, status=400)


@login_required
def mon_compte(request):
    user = request.user
    if user.groups.exists():
        group = user.groups.all()[0].name       
        if group == 'Doctor':
            # print('doctor is part of the staff')
            # Send back the next appointments
            my_appointments = Appointment.objects.all().order_by('date')
            paginator = Paginator(
                my_appointments.order_by('start_time'), 
                APPOINTMENTS_PER_PAGE
            )
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, "podologie/staff.html", {
                'my_appointments': page_obj
            })
    patient = Patient.objects.get(user=user)
    my_appointments = Appointment.objects.filter(patient=patient).order_by('date')
    return render(request, "podologie/mon_compte.html", {
        'my_appointments': my_appointments.order_by('start_time') 
    })
    
@login_required
def delete_appointment(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        appointment_pk = data.get('appointmentPK')
        try:
            appointment = Appointment.objects.get(pk=appointment_pk)
            appointment.delete()
        except IntegrityError as e:
            print(e)
            return JsonResponse({'message':'Something went wrong'}, status=400)
        return JsonResponse({'obj_id': appointment_pk}, status=200)

def available_ts(request):
    """
    API consumed by JS
    Method to check if there are appointment(s) time slot already taken on a particular date.
    Return and populate accordingly the list of timeslots to client side.
    """  
    
    if request.method == "GET":        
        date = request.GET.get("date")
        service = request.GET.get("service")         
        # DB Formatting 
        dt = pd.Timestamp(date)
        # Get service
        service_obj = Service.objects.filter(motif=service).first()        
        # Get duration of the service (motif de consultation)
        service_duration = int(service_obj.timing.split(' ')[0])
        # Get appointments 
        appointments = Appointment.objects.filter(date=dt).all()
        # Get appointments times
        appointments_times = []
        if appointments.exists():
            for appointment in appointments.iterator():
                # TZinfo set to None from DB appointments "offset aware" datetime objects, 
                # because all other datetime objects are "offset naive"
                appointments_times.append((
                    appointment.start_time.replace(tzinfo=None), 
                    appointment.end_time.replace(tzinfo=None)
                ))        
        # Day schedule
        hours = day_hours(
            date, 
            START_TIME, 
            END_TIME
        )
        pause = day_pause(
            date, 
            PAUSE_START_TIME, 
            PAUSE_END_TIME
        )
        available_slots = get_slots(
            hours, 
            appointments_times, 
            pause, 
            duration=datetime.timedelta(minutes=service_duration)
        ) 
        return JsonResponse({
            'message':'Slots of the day for the selected service',
            'timeslotList': available_slots      
            }, status = 200)            
    return JsonResponse({'message':'Someting went wrong'}, status=404)

@login_required
def create_appointment(request):
    """
    API endpoint to create and book an appointment
    """
    if request.method == "POST":        
        # Note : add control to prevent a user to book multiple appointment the same day ?        
        ## Note bis : further check if dates is not a closed date (to be sure)        
        data = json.loads(request.body)
        service = data.get('service')
        date = data.get('date')  
        precisions = data.get('precisions')      
        # Date Formatting
        dt= pd.Timestamp(date)        
        date= date.split('-')
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])        
        timeslot = data.get('timeslot') # 10:30 - 11:30        
        startslot = timeslot.split('-')[0].strip()
        endslot = timeslot.split('-')[1].strip()
        start_hour = int(startslot.split(':')[0])
        start_minutes = int(startslot.split(':')[1])
        end_hour = int(endslot.split(':')[0])
        end_minutes = int(endslot.split(':')[1])        
        start = datetime.datetime.combine(
            datetime.date(year, month, day), 
            datetime.time(start_hour, start_minutes)
        )
        end = datetime.datetime.combine(
            datetime.date(year, month, day), 
            datetime.time(end_hour, end_minutes)
        )              
        # print('INFOS:' + service, date, timeslot, precisions)        
        # Creating and saving object to database
        try :
            appointment = Appointment.objects.create(
                date = dt.replace(tzinfo=pytz.UTC),
                start_time = start.replace(tzinfo=pytz.UTC),
                end_time = end.replace(tzinfo=pytz.UTC),
                motif = Service.objects.get(motif=service),
                patient = Patient.objects.get(user=request.user), 
                precisions = precisions,               
            )
            appointment.save()
            
            # Send mail
            send_mail(
                 'RDV - PODOLOGIE', #'Subject here',
                 'Bonjour, nous confirmons votre rendez-vous le {},de {}h à {}h pour {}'.format(date, startslot, endslot, service), #'Here is the message.',
                 '',
                 [request.user.email],
                 fail_silently=False,
            )
            # Listen locally for mail sending
            # python -m smtpd -n -c DebuggingServer localhost:1025
        except IntegrityError as e:
            print(e)
            return JsonResponse({'message':'Something went wrong'}, status=400)
    return JsonResponse({}, status=200)
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("podologie:index"))
        else:
            return render(request, "podologie/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "podologie/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("podologie:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        last_name = request.POST["lastname"]
        email = request.POST["email"]
        # Note : maybe further control on email validity

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "podologie/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            # Create a patient profile :
            patient = Patient.objects.create(user = user)
            patient.firstname = username
            patient.lastname = last_name
            patient.save()
        except IntegrityError:
            return render(request, "podologie/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("podologie:index"))
    else:
        return render(request, "podologie/register.html")
    
    
    
