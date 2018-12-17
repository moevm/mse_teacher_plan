function showPlans() {
    let slider = $("#year_slider");
    let obj = {
        user_id: $("#user_select").val(),
        year_start: slider.slider('values', 0),
        year_end: slider.slider('values', 1)
    };
    $.ajax({
        url: '/plans',
        method: 'GET',
        data: obj,
        success: (response)=>{
            if (response.ok)
                printPlans(response.plans)
        }
    })
}

var simple = false;
const simple_length = 2;

function toggleSimple(){
    let button = $("#full_button");
    if (!simple){
        button.removeClass('btn-primary');
        button.addClass('btn-success');
        button.text('Вывод: меньше');
        simple = true;
    }
    else {
        button.addClass('btn-primary');
        button.removeClass('btn-success');
        button.text('Вывод: всё');
        simple = false;
    }
}

function printPlans(plans_obj){
    let plans_container = $("#plans_container");
    plans_container.empty();
    let plans_accordion = $('<div>');
    plans_obj.forEach((plan_type)=>{
        if (plan_type.plans.length > 0) {
            let header = $('<h3>').text(plan_type.text);
            let accordion_content = $('<div>');
            let plans_table = generatePlanTable(plan_type);
            accordion_content.append(plans_table);
            plans_accordion.append(header, accordion_content);
        }
    });
    if (plans_obj.length === 0){
        plans_accordion.append($('<h3>').text('Планов нет'))
    }
    else {
        plans_accordion.accordion({
            heightStyle: "fill"
        });
    }
    plans_container.append(plans_accordion);
}

function generatePlanTable(plan_type, add_year = true, add_controls = true) {
    let plans_table = $("<table>").addClass('table');
    let table_header = $("<thead>").addClass('thead-light').append("<tr>");
    if (add_year)
        table_header.append($("<th>").attr('scope', 'col').text('Год'));
    for (field of plan_type.plans[0]){
        if (field.text !== '%NO_VERBOSE_NAME%')
            table_header.append($("<th>").attr('scope', 'col').text(field.text));
        if (simple && table_header.children().length > simple_length)
            break
    }
    if (add_controls)
        table_header.append($("<th>").attr('scope', 'col').text('Управление'));
    plans_table.append(table_header);

    let table_body = $("<tbody>");
    for (plan of plan_type.plans){
        let row = generatePlanRow(plan, add_year, add_controls);
        table_body.append(row);
    }
    plans_table.append(table_body);
    return plans_table;
}

function generatePlanRow(plan, add_year, add_controls) {
    let row = $("<tr>");
    let plan_fields = [];
    let plan_id = null;
    let index = 0;
    for (field of plan){
        if (field.text !== '%NO_VERBOSE_NAME%') {
            plan_fields.push($("<td>").text(field.value));
            index++;
        }
        else if ((field.name === 'year') && add_year) {
            let year_field = $("<th>").attr('scope', 'row').text(field.value);
            row.append(year_field);
            index++;
        }
        else if (field.name === 'id') {
            plan_id = field.value;
        }
        if (simple && index >= simple_length)
            break;
    }
    row.append(plan_fields);
    if (add_controls) {
        let button_size = 24;
        let edit_image = $("<img src='/static/icons/edit.png' alt='EDIT'>")
            .css('height', `${button_size}px`).css('width', `${button_size}px`)
            .attr('title', 'Редактировать план');
        let delete_image = $("<img src='/static/icons/trash.png' alt='DEL'>")
            .css('height', `${button_size}px`).css('width', `${button_size}px`)
            .attr('title', 'Удалить план');
        let edit_button = $("<a>").addClass("btn btn-sm btn-primary").attr('href', `/plan?id=${plan_id}`);
        let delete_button = $("<a>").addClass("btn btn-sm btn-danger").attr('onclick', `deletePlan("${plan_id}")`);
        edit_button.append(edit_image);
        delete_button.append(delete_image);
        row.append($("<th>").append($("<div>").addClass("btn-group").append(
            edit_button,
            delete_button
        )))
    }
    return row;
}


function deletePlan(id){
    $.ajax({
        'url': '/plan',
        'method': 'DELETE',
        'dataType': 'json',
        processData: false,
        'contentType': 'application/json',
        'data': JSON.stringify({id: id}),
        success: (json) =>{
            if (!json.ok)
                showErrorDialog(json.data);
            else{
                showPlans();
            }
        }
    })
}