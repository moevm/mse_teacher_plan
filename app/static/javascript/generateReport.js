var report_units;

function getAvailableReportUnits(){
    $.ajax({
        url: '/reportunits',
        method: 'GET',
        success: (response)=>{
            if (response.ok){
                report_units = response.units;
                initReportFilter();
            }
        }
    })
}

function initReportFilter() {
    let list_all = $("<ul>").addClass('connectedSortable').addClass('unit_sortable')
        .attr('id', 'list_all');
    let list_config = $("<ul>").addClass('connectedSortable').addClass('unit_sortable')
        .attr('id', 'list_config');
    for (let unit of report_units){
        let elem = $("<li>").text(unit.text).addClass('ui-state-default').data('value', unit.name);
        list_all.append(elem);
    }
    // noinspection JSUnresolvedFunction
    list_all.sortable({
        connectWith: ".connectedSortable"
    }).disableSelection();
    // noinspection JSUnresolvedFunction
    list_config.sortable({
        connectWith: ".connectedSortable"
    }).disableSelection();
    $("#empty_container").empty().append(list_config);
    $("#config_container").empty().append(list_all);
}

function getSelectedUnits(){
    let list_config = $("#list_config");
    let res = [];
    list_config.children().each(function(){res.push($(this).data('value'))});
    return res;
}

function previewReport(){
    toggleLoading();
    let selected_units = getSelectedUnits();
    $.ajax({
        url: '/report',
        data: JSON.stringify({
            units: selected_units,
            user_id: $("#user_select").val()
        }),
        method: 'POST',
        dataType: 'json',
        processData: false,
        contentType: 'application/json',
        success: (res)=>{
            toggleLoading();
            if (res.ok) {
                $("#preview_report_card").removeAttr('hidden');
                let preview = $("#preview_report");
                preview.empty();
                let iframe = $('<iframe>').attr('srcdoc', res.html).css('width', '100%')
                    .css('height', '800px');
                preview.append(iframe)
            }
        }
    })
}

function getPDF(){
    toggleLoading();
    let selectedUnits = getSelectedUnits();
    $.ajax({
        url: '/reportToPdf',
        data: JSON.stringify({
            units: selectedUnits,
            user_id: $("#user_select").val()
        }),
        method: 'POST',
        dataType: 'json',
        processData: false,
        contentType: 'application/json',
        success: (res)=>{
            toggleLoading();
            if (res.ok){
                window.open(res.url, '_blank');
            }
        }
    })
}

$(document).ready(function () {
    getAvailableReportUnits();
});