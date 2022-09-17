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

// ===================   enable or disable two-factor authentication ======

$(document).on('click', "#approve-button", function () {
    var _vm=$(this);
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/enable-2-authentication",
        dataType: 'json',
        beforeSend:function () {
            _vm.text("loading");
        },
        success: function (res) {
            console.log(res)
            if(res.status === true){
                _vm.text("enable");
                _vm.removeClass('btn btn-danger').addClass('btn btn-info');
                _vm.removeClass('disabled');
            }else {
                _vm.text("disable");
                _vm.removeClass('btn btn-info').addClass('btn btn-danger');
                _vm.removeClass('disabled');
            }

        }
    })
});