function showPlans() { //TODO
    let slider = $("#year_slider");
    obj = {
        'user_id': $("#user_select").val(),
        'year_start': slider.slider('values', 0),
        'year_end': slider.slider('values', 1)
    };
    $.ajax({
        url: '/plans',
        method: 'GET',
        data: obj,
        dataType: 'json',
        processData: false,
        contentType: 'application/json'
    })
}
