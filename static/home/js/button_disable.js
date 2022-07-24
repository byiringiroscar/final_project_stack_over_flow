const checkboxButton = document.querySelector('#approve-terms')
const approveSubmitButton = document.querySelector('#approve-button')


checkboxButton.addEventListener('click', function (){
    if(checkboxButton.checked){
    approveSubmitButton.removeAttribute("disabled");
    }
    else {
        approveSubmitButton.disabled = true;
    }
})

