hideSidebar();

function submitInfo() {
    let obj = {};
    for (let i=0; i < profile.length; i++){
        let name = 'profile_' + profile[i].name;
        let elem = document.getElementById(name);
        if (elem) {
            if (elem.type !== 'select-one')
                obj[profile[i].name] = elem.value;
            else{
                obj[profile[i].name] = $("#" + elem.value).text().replace(/[\r?\n\s]/g, "")
            }

        }
    }
    $.ajax({
        'url': '/registration',
        'method': 'POST',
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