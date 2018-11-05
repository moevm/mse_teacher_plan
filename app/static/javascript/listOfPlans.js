function showPlans() { //TODO
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

function printPlans(plans_obj){
    let plans_container = $("#plans_container");
    plans_container.empty();
    let plans_accordion = $('<div>');
    plans_obj.forEach((plan_type)=>{
        let header = $('<h3>').text(plan_type.text);
        let accordion_content = $('<div>');
        let plans_table = generatePlanTable(plan_type);
        accordion_content.append(plans_table);
        plans_accordion.append(header, accordion_content);
    });
    plans_accordion.accordion({
        heightStyle: "fill"
    });
    plans_container.append(plans_accordion);
}

function generatePlanTable(plan_type, add_year = true, add_controls = true) {
    let plans_table = $("<table>").addClass('table');
    let table_header = $("<thead>").addClass('thead-light').append("<tr>");
    if (add_year)
        table_header.append($("<th>").attr('scope', 'col').text('Год'));
    plan_type.plans[0].forEach((field) => {
        if (field.text !== '%NO_VERBOSE_NAME%')
            table_header.append($("<th>").attr('scope', 'col').text(field.text));
    });
    if (add_controls)
        table_header.append($("<th>").attr('scope', 'col').text('Управление'));
    plans_table.append(table_header);
    let table_body = $("<tbody>");
    plan_type.plans.forEach((plan) => {
        let row = generatePlanRow(plan, add_year, add_controls);
        table_body.append(row);
    });
    plans_table.append(table_body);
    return plans_table;
}

function generatePlanRow(plan, add_year, add_controls) {
    let row = $("<tr>");
    let plan_fields = [];
    let plan_id = null;
    plan.forEach((field) => {
        if (field.text !== '%NO_VERBOSE_NAME%')
            plan_fields.push($("<td>").text(field.value));
        else if ((field.name === 'year') && add_year) {
            let year_field = $("<th>").attr('scope', 'row').text(field.value);
            row.append(year_field)
        }
        else if (field.name === 'id') {
            plan_id = field.value;
        }
    });
    row.append(plan_fields);
    if (add_controls) {
        row.append($("<th>").append($("<div>").addClass("btn-group").append(
            $("<a>").addClass("btn btn-sm btn-secondary").text("EDIT").attr('href', `/plan?id=${plan_id}`),
            $("<button>").addClass("btn btn-sm btn-danger").text("DEL").attr('onclick', `deletePlan("${plan_id}")`)
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