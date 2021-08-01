document.addEventListener('DOMContentLoaded', function() {

$.datepicker.setDefaults($.datepicker.regional['fr'])
$("#datepicker").datepicker({
    beforeShowDay: disableDates,       
    changeMonth: true, 
    changeYear: false, 
    dateFormat: 'dd-mm-yy',
    minDate: "+1d",
    maxDate: "+1y",
    onSelect: function(date) {loadTimeSlotsAvailable(date)}
})     

 function disableDates(date) {
    // Note : ClosedDates is initialized on window.load via an API ending point.
    // let ClosedDates = ["03-08-2021", "04-08-2021"];
    let noWeekend = jQuery.datepicker.noWeekends(date);
    let dt = $.datepicker.formatDate('dd-mm-yy', date);   
    // Jquery forum
    return noWeekend[0] ? (($.inArray(dt, ClosedDates) < 0) ? [true] : [false]) : noWeekend;
}

const handleErrors = (response) => {
    //console.log(response)
    if (!response.ok) throw new Error(response.error);
    return response;
}

const loadTimeSlotsAvailable = (date) => { 
    document.querySelector('#message').style.display = 'none'   
    // API call
    // Send a GET request to the URL with date and service query parameters
    service = document.querySelector('#available-services').value
    //console.log('API call with: ' + date + ' - ' + service)
    fetch(`http://127.0.0.1:8000/api/available_ts?date=${date}&service=${service}`)
    .then(response => handleErrors(response))
    .then(response => response.json())    
    .then(data => {
        clearAvailableTimeslots();
        // Case when there is no slots available : Nothing will be displayed 
        if (data.timeslotList.length === 0) {
            //console.log('pas de créneaux')
            document.querySelector('#message').style.display = 'block';
        }
        else {
            document.querySelector('#message').style.display = 'none';
            (data.timeslotList).forEach(slot => displayAvailableTimeslots(slot))
        }
            
    })          
    .catch(error => console.log(error))
} 

const clearAvailableTimeslots = () => {
    if (document.querySelector('#available-timeslots').options.length != 0) {
        console.log('list is not empty')
        document.querySelector('#available-timeslots').options.length = 0
    }
}

const displayAvailableTimeslots = (slot) => {
    //console.log(slot)  
    document.querySelector('#slot-form').style.display = 'block'
    let ElementTimeSlot = document.createElement('option')
    ElementTimeSlot.text = slot
    ElementTimeSlot.id = slot
    ElementTimeSlot.value = slot
    document.querySelector('#available-timeslots').appendChild(ElementTimeSlot)   
    document.querySelector('#btn-form-validation').disabled = false
}

// constantes breadcrumb nav
const consultation = document.querySelectorAll('.consult')
const horaire = document.querySelectorAll('.horaire')
const information = document.querySelectorAll('.information')
const validation = document.querySelectorAll('.validation')

// Initial breadcrumb display (@media 2 breadcrumbs)
consultation.forEach( (el) => { el.classList.add('active') })
//consultation.classList.add('active')

// constante pages formulaires
const Page1 = document.querySelector('#page-1')
const Page2 = document.querySelector('#page-2')
const Page3 = document.querySelector('#page-3')
const Page4 = document.querySelector('#page-4')

// constante boutton navigation formulaire
const btnFormValidation = document.querySelector('#btn-form-validation')


// Initial forms display
Page1.style.display = 'block';
Page2.style.display = 'none';
Page3.style.display = 'none';
Page4.style.display = 'none';
    
// Initial navigation form button display
btnFormValidation.innerHTML = "Choisir cette consultation"


btnFormValidation.addEventListener('click', () => DisplayDateForm())

const DisplayDateForm = () => {        

    // Initial breadcrumb display
    horaire.forEach( (el) => { el.classList.add('active') })

    // Form display 
    Page1.style.display = 'none';
    Page2.style.display = 'block';
    Page3.style.display = 'none';
    Page4.style.display = 'none';

    // Button display
    btnFormValidation.innerHTML = "Reserver ce RDV";

    // Constante caldrier et horaires
    const SlotForm = document.querySelector('#slot-form')

    // Initially hide hour slots form and btnForm Validation
    SlotForm.style.display = 'none'       
    btnFormValidation.disabled = true

    // When both date and time are selected it goes to confirmation page        
    btnFormValidation.addEventListener('click', () => DisplayInformationsForm())
}

const DisplayInformationsForm = () => {
    
    // Initial breadcrumb display
    information.forEach( (el) => { el.classList.add('active') })

    // Form display 
    Page1.style.display = 'none';
    Page2.style.display = 'none';
    Page3.style.display = 'block';
    Page4.style.display = 'none';

    // Appointments infos
    const service = document.querySelector('#available-services').value
    const date = document.querySelector('#datepicker').value
    const timeslot = document.querySelector('#available-timeslots').value

    // Buttons display

    btnFormValidation.disabled = false
    btnFormValidation.innerHTML = "Confirmer ces informations";

   
    btnFormValidation.addEventListener('click', () => AppointmentValidation(service, date, timeslot))

    // Display infos
    document.querySelector('#service-confirm').innerHTML = service
    document.querySelector('#date-confirm').innerHTML = date
    document.querySelector('#slot-confirm').innerHTML = timeslot

}

const AppointmentValidation = (service, date, timeslot) => {

    // Initial breadcrumb display
    validation.forEach( (el) => { el.classList.add('active') })

    // Form display 
    Page1.style.display = 'none';
    Page2.style.display = 'none';
    Page3.style.display = 'none';
    Page4.style.display = 'block';

    // Button display    
    btnFormValidation.style.display = 'none'

    // Last (optional) form input
    const precisions = document.querySelector('#precisions').value

    // Creation of an appointment through API endpoint
    CreateAppointment(service, date, timeslot, precisions)
}

const CreateAppointment = (service, date, timeslot, precisions) => {
    // API endpoint
    fetch(`http://127.0.0.1:8000/api/create_appointment/`, {
        method: 'POST',
        headers: {"X-CSRFToken": csrftoken},
        body: JSON.stringify({
            service: service,
            date: date,                
            timeslot: timeslot,
            precisions: precisions
        })
    })
    .then(response => response.json())
    .catch(error => console.log(error))
}

})

