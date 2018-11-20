$(function(){
    let user_handle = $("#user_slider_handle");
    $("#user_slider").slider({
        create: function() {
            user_handle.text( $( this ).slider( "value" ) );
        },
        slide: function( event, ui ) {
            user_handle.text( ui.value );
        },
        min: 1,
        max: 20
    });
    let plans_handle = $("#plans_slider_handle");
    $("#plans_slider").slider({
        create: function() {
            plans_handle.text( $( this ).slider( "value" ) );
        },
        slide: function( event, ui ) {
            plans_handle.text( ui.value );
        },
        min: 1,
        max: 50
    });
});

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

function fillDB() {
    let obj = {
        users: $("#user_slider").slider("value"),
        plans: $("#plans_slider").slider("value")
    };
    $.ajax({
        url: '/fakedata',
        method: 'POST',
        processData: false,
        'contentType': 'application/json',
        'data': JSON.stringify(obj),
    })
}