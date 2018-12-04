let toggled_once = false;
let toggled = false;
function toggleLoading(){
    let modal = $("#loadingModal");
    if(!toggled_once){
        modal.modal({
            backdrop: 'static',
            keyboard: false
        });
        toggled_once = true;
        toggled = true;
    }
    else{
        customToggle();
    }
}

function customToggle(){
    if (!toggled){
        $("#loadingModal").modal('toggle');
        toggled = true;
    }else{
        if (!(($("#loadingModal").data('bs.modal') || {})._isShown)){
            setTimeout(()=>{customToggle()}, 250)
        }
        else{
            setTimeout(()=>{$("#loadingModal").modal('toggle')}, 300);
        }
        toggled = false;
    }
}