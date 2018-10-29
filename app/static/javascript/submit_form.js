function submitInfo(form_name, url, init_object, method='POST', add_info=null) {
    let obj = {};
    for (let i=0; i < init_object.length; i++){
        let name = form_name + '_' + init_object[i].name;
        let elem = document.getElementById(name);
        if (elem) {
            if (elem.type !== 'select-one')
                obj[init_object[i].name] = elem.value;
            else{
                obj[init_object[i].name] = clear($("#" + elem.value).text())
            }
        }
        else if (init_object[i].value){
            obj[init_object[i].name] = init_object[i].value
        }
    }
    if (add_info)
        obj['add_info'] = add_info;
    $.ajax({
        'url': url,
        'method': method,
        'dataType': 'json',
        processData: false,
        'contentType': 'application/json',
        'data': JSON.stringify(obj),
        success: (json) =>{
            if (!json.ok)
                showErrorDialog(json.data);
            else
                window.open('/', '_self')
        }
    })
}

function clear(text) {
    text = text.replace(/([\n\s]+$)/g, "").replace(/^([\n\s]+)/g, "")
    return text
}