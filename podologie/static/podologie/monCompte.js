document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#supprimer').forEach(btn => {
        btn.addEventListener('click', (e) => AskForValidation(e))
    })


const AskForValidation = (e) => {
    const id = e.target.value
    const btn = e.target
    const btnYES = document.createElement('button')
    const btnNO = document.createElement('button')
    const validationDiv = document.createElement('div')
    validationDiv.className = 'd-grid gap-2 col-6 mx-auto mt-4'
    validationDiv.style.background = '#ffffff'
    btn.innerHTML = 'Confirmer mon annulation ?'
    btn.style.color = '#ffffff'
    btn.style.background = '#ed1c24'
    btn.disabled = true    
    btnYES.innerHTML = 'OUI'   
    btnYES.className = "btn btn-secondary btn-xs"
    btnNO.innerHTML ='NON'
    btnNO.className = "btn btn-secondary btn-xs"
    validationDiv.append(btnYES, btnNO)
    btn.append(validationDiv)
    // btn.append(btnNO)
    btnYES.addEventListener('click', () => DeleteAppointment(id))
    btnNO.addEventListener('click', () => ReturnNormalDisplay(btn, btnYES, btnNO))
}


const ReturnNormalDisplay = (btn, btnYES, btnNO) => {
    btn.disabled = false
    btn.innerHTML = 'Annuler mon rdv'
    btn.style.removeProperty('color')
    btn.style.removeProperty('background')
    btnYES.remove()
    btnNO.remove()
}

const DeleteAppointment = (id) => {
    // API call
    fetch(`http://127.0.0.1:8000/api/delete_appointment/`, {
        method: 'DELETE',
        headers: {"X-CSRFToken": csrftoken},
        body: JSON.stringify({
            appointmentPK: id,
        })
    })
    .then(response => HandleResponse(response))
    .then(response => response.json())
    .then(data => removeAppointment(data.obj_id))
    .catch(error => console.log(error))
}
const removeAppointment = (objID) => {
    elToDelete = document.getElementById(objID)
    elToDelete.remove()
}

const HandleResponse = (response) => {
    if (!response.ok) throw new Error(response.error);
    return response;
}
})
