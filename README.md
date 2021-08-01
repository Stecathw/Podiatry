# CAPSTONE PROJECT - PODIATRY WEBSITE

Link to youtube video demo:

https://www.youtube.com/watch?v=aHKf0iKfxl0

Link to project specifications :

https://cs50.harvard.edu/web/2020/projects/final/capstone/

## INTRO

I had several project ideas, from a personal blog to a weather website and many others. But I decided it would be fair enough to get under pressure of a so-called "client", and I knew someone that would need a website for its future dreamed business. Therefore I went straight for that kind of project, and I asked for my "client" precisions. I told my client that this was a challenge for me and that the first version of the site couldn't be the one in final production and delivered. It will require a little more work and improvements and some security checks with a professional dev later. Still, it was okay at this stage to be a final project within CS50W and a maybe future product.

Let's dive in a real life problem.

## DISTINCTIVENESS AND COMPLEXITY

### THE LAYOUT

The website is at first a single page presentation of a podiatry clinic. Client needed a modern design including a sticky navbar, 
an image slider, sections to describe overall jobs, a contact section with a map localisation, a classic footer
and all that responsive stuff.

![alt tag](https://github.com/Stecathw/Podiatry/blob/podologie/static/podologie/images/home.png)

![alt tag](https://github.com/Stecathw/Podiatry/blob/main/podologie/static/podologie/images/footer.png)

Complexity cames with the second requirement including several features. But the general purpose was to allow appointments and keep things as simple and lightest possible.
(We are not building a hospital scheduler either with a huge DB) 

These are the primary features wanted:
- 1/ Visitors could become patient and register, log in and logout and have an acess to a simple patient profile where they can see their future appointment and delete them.
- 2/ The doctor can also log in/ logout and acess a special account to see incoming appointments and close some dates for holidays or ponctual closure purpose. In all calendars, such days shouldn't be selectable.
- 3/ The clinic offers several services and each have different durations (A checkup is 30min long whereas a delivery is 15min or an orthopedic sole modification is 60min)
- 4/ The clinic is daily opened from 9am to 17pm with a pause between 12 to 1pm; closed on staturday and sunday.
- 5/ All visitors can acess to a "Make appointment" page, where they can select a service among the proposed ones, look for available dates and hours, but can't validate and book an appointment if they are logged in.
- 6/ Slots available in the day are calculated knowing daily routine schedule, services durations and others potentially taken appointments.
- 7/ Logged visitors (patient) can book an appointment and both the doctor and the patient will receive an email confirmation.
- 8/ The make appointment page should also be fully responsive and a single page dynamic form.

![alt tag](https://github.com/Stecathw/Podiatry/blob/main/podologie/static/podologie/images/form3.png)

### TECHNOLOGIES USED

For simplicity, I decided to keep React away as it is adding unecessary complexity when creating a pipeline and connecting it to Django. 
So, the frontend is mostly handled by plain Javascript.
On the otherhand the backend is handled by Python and everything is of course built uppon Django framework.
I have also used Jquery datepicker, bootstrap and fontawesome.
To make things easier and faster I've also took a free template coming with some styles and pre-written css, 
from "Tooplate.com" and integrate it at my own taste.
I used pandas/numpy to make things easier with date manipulation as I previoulsy used this librairy in a past project. Furthermore it will be usefull to build statistics and export csv files as mentionned in "further improvements".

### CRITICAL CONSTRAINTS ABOUT APPOINTMENTS

At first glance, everything seems pretty straightforward and complexity comes with calendar appointment.
Neither handling a whole database with a 365 days calendar with different timeslots for each ones nor re-build a whole calendar scheduler would have been an easy and fast dev path.
Of course, some python librairies comes "hands in key" but they are mostly to complex, applying their owner logic and it couldn't be ok if it was for any reasons deprecated.

### CALENDAR TO API ENDPOINTS

Jquery datepicker is the UI go to component client side and will communicate with backend through API endpoints. 
On mounting calendar, backend sends back closed day that won't be selectable by users.
On day selection it asks backend for any existing appointments at that date and return accordingly to service duration, all available slots between 9-12am and 13-17pm.
Only available slots for appointment in a dropdown list will be displayed. 
If no slots are available at that date for that service no slots will be displayed. 
Every day is generated when asking for available slots avoiding to create a whole calendar schedule database. 
This function is written under "views.py > def available_ts(request)" and "slots.py".
When validating an appointment a new appointment object is created and will be taken into account when another user is looking for its potential appointment at the same date.
Appointments can only be taken between +1 day to +1 year from current date.

![alt tag](https://github.com/Stecathw/Podiatry/blob/main/podologie/static/podologie/images/form2.png)

After appointment creation and validation a email is sent to user.

![alt tag](https://github.com/Stecathw/Podiatry/blob/main/podologie/static/podologie/images/mail.png)

### MODELS AND DB 

The database is build upon 5 models :
- User
- Patient
- Service
- Appointment
- ClosedDate

### GENERAL ARCHITECTURE

All statics Files lives under static/podologie/.
Directly under, 7 main js files holds forms and accounts stuffs with a styles.css
3 other folders (js/, css/, images/) holds the main website page.
Html templates are divided and built accross differents django templates files.

### SPECIAL ACCESS

A group doctor can be attributted to a registered user (client) for convenience and infos. It allows acess to a special doctor account.
The superuser class can also be given. (has to be determined)
NB. A doctor is currently logged as a special patient and can also test and make appointments.

## FURTHER IMPROVEMENTS :

Several features would be build later (as it requires much more time to develop more features) :
- Django admin display
- Informations, titles and text will be more written later. Images and some display could also be updated.
- Patient can modify informations (mail, name, password) or close their account (for now it will be an admin task if needed)
- Emails for accounts CRUD operations.
- Page not found 404
- Unit tests and selenium tests
- A scheduler to automate deletion of past booked appointment but export them into csv file for statistics analysis.
- Production and deployment


For the purpose of the exercice here : all displayed informations within the website are indeed actually faked and are just for testing and previewing purpose. It's not contractual. As the buisness would be located in France with only french patient, no english language is used client side.

For convenience and easiness regarding this private repo, I've submitted my code with submit50. A new dedicated repository will be created for CI/CD purposes later.
