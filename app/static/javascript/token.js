
function new_token() {
    let type = $("#selectToken").val();
    $.ajax({
        url: '/token',
        method: 'POST',
        processData: false,
        contentType: 'application/json',
        data: JSON.stringify({
            type: type
        }),
        success: (response)=>{
            if (response.ok){
                // noinspection JSUnresolvedVariable
                let key = response.key;
                $("#tokenKey").val(key);
                $("#token_card").collapse('show');
            }
        }
    })
}