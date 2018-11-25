function showModal(header, message){
    $("#messageModalLabel").text(header);
    $("#messageModalBody").text(message);
    $("#messageModal").modal('show');
}