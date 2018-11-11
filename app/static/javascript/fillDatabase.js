function makeFake() {
    let obj = {
        'user_id': $('#user_select').val(),
        'type': $('#selectWork').val()
    };
    $.ajax({
        url: '/fakeplan',
        method: 'POST',
        processData: false,
        'contentType': 'application/json',
        'data': JSON.stringify(obj),
    })
}