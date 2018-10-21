function hideSidebar() {
    $("#content_block").removeClass("col-md-9");
    $("#content_block").addClass("col-md-12");
    $("#sidebar_block").hide();
}

function showSidebar() {
    $("#content_block").addClass("col-md-9");
    $("#content_block").removeClass("col-md-12");
    $("#sidebar_block").show();
}

function showErrorDialog(text){  // TODO
    alert(text);
}