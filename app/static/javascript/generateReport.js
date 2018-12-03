var report_types;

function getAvailableReports(){
    $.ajax({
        url: '/reporttypes',
        method: 'GET',
        success: (response)=>{
            if (response.ok) {
                report_types = response.types;
                initReportFilter();
            }
        }
    })
}

function initReportFilter() {
    let list = $("#type_select");
    for(let report_type of report_types){
        let option = $("<option>").val(report_type.name).text(report_type.text);
        list.append(option)
    }
}

function previewReport(){
    toggleLoading();
    let chosen_type = $("#type_select").val();
    $.ajax({
        url: '/report',
        data: {
            type: chosen_type,
            user_id: $("#user_select").val()
        },
        method: 'GET',
        success: (res)=>{
            toggleLoading();
            $("#preview_report_card").removeAttr('hidden');
            let preview = $("#preview_report");
            preview.empty();
            let iframe = $('<iframe>').attr('srcdoc', res).css('width', '100%')
                .css('height', '800px');
            preview.append(iframe)
        }
    })
}

function getPDF(){
    let chosen_type = $("#type_select").val();
    toggleLoading();
    $.ajax({
        url: '/reportToPdf',
        data: {
            type: chosen_type,
            user_id: $("#user_select").val()
        },
        method: 'GET',
        success: (res)=>{
            toggleLoading();
            if (res.ok){
                window.open(res.url, '_blank');
            }
        }
    })
}

$(document).ready(function () {
    getAvailableReports();
});