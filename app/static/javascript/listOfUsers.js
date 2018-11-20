function getUsers(active_section = 0){
    $.ajax({
        url: '/userlist',
        method: 'GET',
        success: (response)=>{
            if (response.ok)
                printUsers(response.users, active_section)
        }
    })
}

function printUsers(users, active_section) {
    let sorted = sortByType(users);
    let attrs = [
        {'name': 'login', 'text': 'Логин'},
        {'text': 'Имя'},
        {'text': 'Фамилия'},
        {'text': 'Учебное звание'}
    ];
    let container = $("#users_container");
    container.empty();
    createAccordion(sorted, container, attrs, true, active_section);
    console.log(sorted);
}


function sortByType(users){
    function getUserTypes(user) {
        for(let field of user.profile){
            if (field.name === 'type') {
                return field.opts
            }
        }
    }
    function getType(user){
        for (let i = 0; i < user.profile.length; i++){
            if (user.profile[i].name === 'type'){
                let type = user.profile[i].value;
                // user.profile.splice(i, 1);
                return type;
            }
        }
    }
    let types = getUserTypes(users[0]);
    let res = [];
    types.forEach((type)=>{
        res.push({
            'name': type,
            'users': []
        })
    });
    users.forEach((user)=>{
        let type = getType(user);
        res.forEach((type_cont)=>{
            if (type_cont.name === type){
                type_cont.users.push(user);
            }
        })
    });
    return res;
}

function createAccordion(sorted, container, attrs, add_controls=false, active=0){
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
        active: active
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
            row.append($("<th>").append($("<div>").addClass("btn-group").append(
                $("<a>").addClass("btn btn-sm btn-secondary").text("EDIT"),
                $("<button>").addClass("btn btn-sm btn-danger").text("DEL").attr('onclick', `deleteUser("${user_id}")`)
            )))
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
                    let active = $('#user_accordion').accordion("option", 'active');
                    getUsers(active)
                }
            }
        }
    })
}

getUsers();