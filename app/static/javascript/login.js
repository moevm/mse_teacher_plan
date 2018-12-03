hideSidebar();
$('#login_button').click((event)=>{
    const form = $("#login_form");
    toggleLoading();
    if (form[0].checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation()
    }
    form.addClass('was-validated');
    obj = {
        'login': $('#login_input').val(),
        'password': $("#password_input").val()
    };
    console.log(obj);
    $.ajax({
        'url': '/login',
        'method':'POST',
        'dataType': 'json',
        processData: false,
        'contentType': 'application/json',
        'data': JSON.stringify(obj),
        success: (json) =>{
            toggleLoading();
            if (!json.ok)
                showErrorDialog(json.data);
            else
                location.reload()
        }
    });
    event.preventDefault();
});