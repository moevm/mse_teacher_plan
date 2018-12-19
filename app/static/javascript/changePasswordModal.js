function savePassword() {
    let old = $("#old_password").val();
    let new_1 = $("#new_password").val();
    let new_2 = $("#repeat_password").val();
    if (new_1 === new_2){
        $.ajax({
            url: '/password',
            method: 'PUT',
            data: JSON.stringify({
                old_pass: old,
                new_pass: new_1
            }),
            dataType: 'json',
            processData: false,
            contentType: 'application/json',
            success: (response)=>{
                if (response.ok)
                    location.reload();
                else
                    showErrorDialog(response.message)
            }
        })
    }
}
function checkPassword(e){
    let pass = $("#new_password").val();
    if (pass !== e.target.value){
        $(e.target).addClass('alert-danger')
    }
    else{
        $(e.target).removeClass('alert-danger')
    }
}