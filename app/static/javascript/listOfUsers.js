var users;
var active_section = 0;

function getUsers(){
    $.ajax({
        url: '/userlist',
        method: 'GET',
        success: (response)=>{
            if (response.ok) {
                users = response.users;
                users[0].user[1].text = 'Логин';
                initFilter();
            }
        }
    })
}

function getUsersAndPrint(){
    $.ajax({
        url: '/userlist',
        method: 'GET',
        success: (response)=>{
            if (response.ok) {
                users = response.users;
                users[0].user[1].text = 'Логин';
                printUsers()
            }
        }
    })
}



function initFilter() {
    let selects = $("#fields_select");
    let sort_options = $("#type_select");
    let index = 0;
    function addField(field) {
        if (field.text !== "%NO_VERBOSE_NAME%") {
            let checkbox = $("<input>").addClass('form-check-input').attr('type', 'checkbox').attr('value', field.name).
            attr('id', `use_${field.name}`);
            if (index++ < 4)
                checkbox.attr('checked', '');
            selects.append($("<div>").addClass('form-check').append(
                checkbox
            ).append(
                $("<label>").addClass('form-check-label').attr('for', `use_${field.name}`).text(field.text)
            ));
            if (field.opts.length > 0){
                sort_options.append($('<option>').val(field.name).text(field.text))
            }
        }
    }

    for (let field of users[0].user){
        addField(field);
    }

    for (let field of users[0].profile) {
        addField(field);
    }
}

function readAttrs(){
    let attrs = [];
    for (let field of users[0].user){
        let checkbox = $(`#use_${field.name}`);
        if (checkbox && checkbox.is(':checked')){
            attrs.push({'name' : field.name, 'text': field.text})
        }
    }
    for (let field of users[0].profile){
        let checkbox = $(`#use_${field.name}`);
        if (checkbox && checkbox.is(':checked')){
            attrs.push({'name' : field.name, 'text': field.text})
        }
    }
    return attrs;
}

function printUsers() {
    let sorted = sortBy($("#type_select").val());
    let attrs = readAttrs();
    let container = $("#users_container");
    container.empty();
    createAccordion(sorted, container, attrs, true, 0);
    console.log(sorted);
}

function getField(fields, name){
    for (let field of fields) {
        if (field.name === name)
            return field;
    }
}

function sortBy(field){
    function getAllOptions(user) {
        return getField(user.profile, field).opts;
    }
    function getChosenOption(user) {
        return getField(user.profile, field).value;
    }

    let types = getAllOptions(users[0]);
    let res = [];
    types.forEach((type)=>{
        res.push({
            'name': type,
            'users': []
        })
    });
    users.forEach((user)=>{
        let type = getChosenOption(user);
        res.forEach((type_cont)=>{
            if (type_cont.name === type){
                type_cont.users.push(user);
            }
        })
    });
    return res;
}


function createAccordion(sorted, container, attrs, add_controls=false){
    let accordion = $('<div>').attr('id', 'user_accordion');
    sorted.forEach((type_cont, index)=>{
        let header = $('<h3>').text(`Тип: ${type_cont.name}`);
        let content = $('<div>').attr('id', `acc_${index}`);
        let content_table = generateUserTable(type_cont.users, attrs, add_controls);
        content.append(content_table);
        accordion.append(header, content)
    });
    accordion.accordion({
        heightStyle: "fill",
        active: active_section
    });

    container.append(accordion);
}

function generateUserTable(users, attrs, add_controls) {
    const headerElem = (text) => { return $("<th>").attr('scope', 'col').text(text) };
    function getAttrs(user, attrs){
        let res = [];
        let iterate = (field)=>{
            for (let i = 0; i < attrs.length; i++){
                let attr = attrs[i];
                if (attr.name){
                    if (attr.name === field.name){
                        res[i] = field.value;
                    }
                }
                else{
                    if (attr.text === field.text){
                        res[i] = field.value;
                    }
                }
            }
        };
        user.profile.forEach(iterate);
        user.user.forEach(iterate);
        return res;
    }
    let table = $("<table>").addClass('table');
    let header = $("<thead>").addClass('thead-light').append("<tr>");
    attrs.forEach((attr)=>{
        header.append(headerElem(attr.text));
    });
    if (add_controls){
        header.append(headerElem('Управление'));
    }
    users.forEach((user)=>{
        let row = $("<tr>");
        let user_attrs = getAttrs(user, attrs);
        user_attrs.forEach((user_attr, index)=>{
            let field;
            if (index === 0){
                field = $("<th>").attr('scope', row)
            }
            else{
                field = $("<td>");
            }
            field.text(user_attr);
            row.append(field);
        });
        if (add_controls){
            let user_id = getAttrs(user, [{'name': 'id'}])[0];
            let button_size = 24;
            let edit_image = $("<img src='/static/icons/edit.png' alt='EDIT'>")
                .css('height', `${button_size}px`).css('width', `${button_size}px`)
                .attr('title', 'Редактировать план');
            let delete_image = $("<img src='/static/icons/trash.png' alt='DEL'>")
                .css('height', `${button_size}px`).css('width', `${button_size}px`)
                .attr('title', 'Удалить план');
            let edit_button = $("<a>").addClass("btn btn-sm btn-primary").attr('href', `/profile_edit?user_id=${user_id}`);
            let delete_button = $("<a>").addClass("btn btn-sm btn-danger").attr('onclick', `deleteUser("${user_id}")`)
            edit_button.append(edit_image);
            delete_button.append(delete_image);
            row.append($("<th>").append($("<div>").addClass("btn-group").append(
                edit_button, delete_button)))
        }
        table.append(row);
    });
    table.append(header);
    return table;
}

function deleteUser(user_id){
    $.ajax({
        url: '/user',
        method: 'DELETE',
        dataType: 'json',
        processData: false,
        contentType: 'application/json',
        data: JSON.stringify({id: user_id}),
        success: (response)=>{
            if (response.ok){
                if (response.reload)
                    location.reload();
                else {
                    active_section = $('#user_accordion').accordion("option", 'active');
                    getUsersAndPrint();
                }
            }
        }
    })
}

getUsers();