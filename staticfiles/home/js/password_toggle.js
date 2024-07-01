const showPasswordToggleOn = document.querySelector('.eye-on1')
const showPasswordToggleOff = document.querySelector('.eye-off1')
const password1Toggle = document.querySelector('.password-field')
const password2Toggle = document.querySelector('.password-field1')
const emailField=document.querySelector('#emailField')
const emailFeedBackArea = document.querySelector('.emailFeedBackArea')
const emailSuccessOutput = document.querySelector('.emailSuccessOutput')
const submitBtn = document.querySelector('#send-message-btn')
const usernameField = document.querySelector('#username')
const  feedBackArea = document.querySelector('.invalid-feedback')
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput')
const passwordMatch = document.querySelector('.passwordMatch')
const password1Match = document.querySelector('.passwordMatch1')

// phone number
const phoneNumber = document.querySelector('#phoneNumber')
const phoneFeedBackArea = document.querySelector('.phoneFeedBackArea')
const phoneSuccessOutput = document.querySelector('.phoneSuccessOutput')




// ==================== password toggle ============================
let conTentOn = '';
let contentOff = '';
showPasswordToggleOff.style.display = "none";
const handleToggleInputOn=(e)=> {
    conTentOn = showPasswordToggleOn;
    if(conTentOn === showPasswordToggleOn) {
        showPasswordToggleOn.style.display = "none";
        showPasswordToggleOff.style.display = "block";
        password2Toggle.setAttribute("type", "text")
    }
}

const handleToggleInputOff=(e)=>{
    contentOff = showPasswordToggleOff;
    if(contentOff === showPasswordToggleOff){
        showPasswordToggleOn.style.display = "block";
        showPasswordToggleOff.style.display = "none";
        password2Toggle.setAttribute("type", "password");
    }
}
showPasswordToggleOn.addEventListener('click', handleToggleInputOn);

showPasswordToggleOff.addEventListener('click', handleToggleInputOff);


// =================== email validation ========================

emailField.addEventListener('keyup', (e)=>{
    const emailVal = e.target.value;
    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";
    emailSuccessOutput.style.display = "block";
    if(emailVal.length>0){
        fetch('/authentication/validate-email', {
            body: JSON.stringify({email: emailVal}),
            method: "POST"
        }).then(res=>res.json().then(data=>{
            emailSuccessOutput.style.display="none";
            if(data.email_error){
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display = "block";
                emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
                submitBtn.disabled = true;
            }else {
                submitBtn.removeAttribute("disabled");
            }
        }))
    }
})

// ==================== phone number validation ===========================

phoneNumber.addEventListener('keyup', (e)=>{
    const phoneVal = e.target.value;
    phoneNumber.classList.remove("is-invalid");
    phoneFeedBackArea.style.display = "none";
    if(phoneVal.length>0){
        fetch('/authentication/validate-phone', {
            body:JSON.stringify({phone_number:phoneVal}),
            method: "POST"
        }).then(res=>res.json().then(data=>{
            if(data.phone_error){
                phoneNumber.classList.add("is-invalid");
                phoneFeedBackArea.style.display = "block";
                phoneFeedBackArea.innerHTML = `<p>${data.phone_error}</p>`;
                submitBtn.disabled = true;

            }else {
                submitBtn.removeAttribute("disabled");
            }
        }))
    }
})

// ================ username validation =======================

usernameField.addEventListener('keyup', (e)=>{
    const usernameVal = e.target.value;
    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display="none";
    usernameSuccessOutput.style.display = "block";
    usernameSuccessOutput.textContent=`checking:  ${usernameVal}`
    if(usernameVal.length>0){
        fetch("/authentication/validate-username", {
            body: JSON.stringify({username: usernameVal}),
            method: "POST"
        }).then(res=>res.json().then(data=>{
            usernameSuccessOutput.style.display="none";
            if(data.username_error){
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display="block";
                feedBackArea.innerHTML=`<p>${data.username_error}</p>`;
                submitBtn.disabled = true;
            }else {
                submitBtn.removeAttribute("disabled");
            }
        }));
    }else {
        usernameSuccessOutput.style.display = "none";
    }
});

//  ========================== check if password match =======================

//check password 1 length
password1Toggle.addEventListener('keyup', (e)=>{
    const password1ValCheck = e.target.value;
    if(password1ValCheck.length===0){
        passwordMatch.style.display = "none";
        passwordMatch.textContent = "";
        password2Toggle.disabled = true;
        submitBtn.disabled = true;
    }
    else if(password1ValCheck.length<3){
        passwordMatch.style.display = "block";
        passwordMatch.classList.remove("text-success");
        passwordMatch.classList.add("text-danger");
        passwordMatch.textContent = "password too small";
        password2Toggle.disabled = true;
        submitBtn.disabled = true;
    }
    else {
        passwordMatch.style.display = "none";
        passwordMatch.classList.remove("text-danger");
        passwordMatch.classList.add("text-success");
        password2Toggle.removeAttribute("disabled");

    }
});


// ============ password 2 check overall ==========

password2Toggle.addEventListener('keyup', (e)=>{
    const password2Value = e.target.value;
    let password1Value = password1Toggle.value;
    if(password2Value.length===0){
        password1Match.textContent = '';
        submitBtn.disabled = true;
    }
    else if(password1Value.length>3){
        if(password2Value === password1Value){
                password1Match.classList.remove("text-danger");
                password1Match.classList.add("text-success");
                password1Match.textContent = 'password match';
                submitBtn.removeAttribute("disabled");
        }else {
            password1Match.classList.remove("text-success");
            password1Match.classList.add("text-danger");
            password1Match.textContent = 'password not match';
            submitBtn.disabled = true;
        }
    }else if(password2Value.length<2){
        password1Match.textContent = '';
    }else {
        console.log("see");
    }


})
