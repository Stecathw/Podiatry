let ClosedDates;

window.onload = () => {
   fetch(`http://127.0.0.1:8000/api/get_unavailability/`)
    .then(response => response.json())
    .then(data => {
        ClosedDates = data.dates;
        // console.log(ClosedDates)
    })          
    .catch(error => console.log(error))    
}