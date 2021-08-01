document.addEventListener('DOMContentLoaded', function() {

    if (document.querySelector('#valider')) {
        document.querySelector('#valider').addEventListener('click', () => { 
            MakeUnavailableDays()      
        })
    }
    const MakeUnavailableDays = () => {
        let startDate = document.querySelector('#alternate_start').value
        let endDate = document.querySelector('#alternate_end').value
        console.log(startDate, endDate)
        // API endpoint to create and store date of closures in DB
        fetch(`http://127.0.0.1:8000/api/close_dates/`, {
            method: 'POST',
            headers: {"X-CSRFToken": csrftoken},
            body: JSON.stringify({
                start: startDate,
                end: endDate,              
            })
        })
        .then(response => response.json())
        .catch(error => console.log(error))
    }
})


