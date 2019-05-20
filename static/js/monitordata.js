$(document).ready(function(){
    if ( $("#select_host_ip").length > 0 ) {
        var selectText = "";
        selectText += "<option data-hidden='true' disabled selected>Search Server.</option>";
        $("#select_host_ip option:first").before(selectText);
    }
    $("#search_info").hide();
});

$("#hostmode_form").click(function(){
    if ( $("#select_host_ip option:selected").prop("disabled") == false ) {
        var search_text = $("#select_host_ip option:selected").text();
        var search_val = $("#select_host_ip option:selected").val();
        var search_title = "<i class='fa fa-yelp'></i>" + "&nbsp Information For &nbsp" + "<strong>"
            + search_text + "</strong>";
        $.ajax({
            url: '/monitor/s',
            type: 'POST',
            dataType: 'json',
            data: {'type':"host", 'option': search_val}
        })
        $("#search_info_title").html(search_title);
        $("#search_info").show();
    }
});

$("#monitordata_hostmode").click(function() {
    window.location.reload();
});

$("#monitordata_cpu").click(function() {
    CreateTableFunc();
    $.ajax({
        url: '/monitor/s',
        type: 'POST',
        dataType: 'json',
        data: {'type':"cpu",'option':"percent"},
        success: DataFunc
    });
});

$("#monitordata_memory").click(function(){
     CreateTableFunc();
     $.ajax({
         url: '/monitor/s',
         type: 'POST',
         dataType: 'json',
         data: {'type':"memory",'option':"GB"},
         success: DataFunc
     });
});

$("#monitordata_disk").click(function(){
     CreateTableFunc();
     $.ajax({
         url: '/monitor/s',
         type: 'POST',
         dataType: 'json',
         data: {'type':"disk"},
         success: DataFunc
     });
});

$("#monitordata_network").click(function(){
     CreateTableFunc();
     $.ajax({
         url: '/monitor/s',
         type: 'POST',
         dataType: 'json',
         data: {'type':"network"},
         success: DataFunc
     });
});

function CreateTableFunc() {
    if ($("#card-table").length > 0) {
        console.log("find card-table");
    } else {
        var cardText = "";
        cardText += '<div class="card mb-8">';
        cardText += '<div class="card-header"></div>';
        cardText += '<div class="card-body">';
        cardText += '<div class="table-responsive">';
        cardText += '<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">';
        cardText += '<thead id="monitortable_thead">';
        cardText += '<tbody id="monitortable_tbody">';
        cardText += '</table></div></div></div>';
        $("#mainSubweb").html(cardText);
    }
}

function DataFunc(data) {
    var titleText = "";
    titleText += "<div><i class='fa fa-table'></i>" + "&nbsp" + data["title"] + "</div>";
    $(".card-header").html(titleText);
    var theadText = "";
    theadText += "<tr>";
    for (var a = 0; a < data["head"].length; a++) {
        var title = data["head"][a];
        theadText += "<td><strong>" + title + "</strong></td>";
    }
    theadText += "</tr>";
    $("#monitortable_thead").html(theadText);
    if ( data["title"] === "Disk List") {
        var diskText = "";
        for (var x=0; x< data["value"].length; x++) {
            var arr = JSON.parse(data["value"][x][2]);
            diskText += "<tr><td>" + data["value"][x][0] + "</td>";
            diskText += "<td><ul class='table-ul'>";
            for (var y=0; y< data["value"][x][1].length; y++) {
                diskText += "<li class='table-ul-li'>" + data["value"][x][1][y] + "</li>";
                if ( y !== arr.length -1 ) {
                    diskText += "<hr class='table-hr' />";
                }
            }
            diskText += "</ul></td><td><ul class='table-ul'>";
            for (var z=0; z< arr.length; z++) {
                diskText += "<li>" + "Used: " + arr[z]["used"] + "</li>";
                diskText += "<li>" + "Total: " +arr[z]["total"] + "</li>";
                diskText += "<li>" + "Percent: " +arr[z]["percent"] + "%" + "</li>";
                diskText += "<li>" + "Inode: " +arr[z]["inode"] + "</li>";
                if ( z !== arr.length -1 ) {
                    diskText += "<hr class='table-hr' />";
                }
            }
            diskText += "</td></ul>";
            diskText += "<td>" + data["value"][x][3] + "</td></tr>";
        }
        $("#monitortable_tbody").html(diskText);
    } else if ( data["title"] === "Network List" ) {
        var netText = "";
        function _netvalue(v1,v2) {
            netText += "<td><ul class='table-ul'>";
            $.each(Arr, function (index, item) {
                if(!v2) {
                    netText += "<li>" + item[v1] + "</li>";
                } else {
                    netText += "<li>" + item[v1] + " / " + item[v2] + "</li>";
                }
                if (index !== Arr.length - 1) {
                    netText += "<hr class='table-hr' />";
                }
            });
            netText += "</ul></td>";
        }
        for (var X=0; X< data["value"].length; X++) {
            var Arr = JSON.parse(data["value"][X][2]);
            netText += "<tr><td>" + data["value"][X][0] + "</td>";
            netText += "<td><ul class='table-ul'>";
            for (var Y=0; Y< data["value"][X][1].length; Y++) {
                netText += "<li>" + data["value"][X][1][Y] + "</li>";
                if ( Y !== Arr.length -1 ) {
                    netText += "<hr class='table-hr' />";
                }
            }
            netText += "</ul></td>";
            // 先手工赋值,后期考虑如何数组传参
            _netvalue("ipaddr");
            _netvalue("speed");
            _netvalue("pps_sent","pps_recv");
            _netvalue("bps_sent","bps_recv");
            _netvalue("errin","errout");
            netText += "<td>" + data["value"][X][3] + "</td>";
        }
        $("#monitortable_tbody").html(netText)
    } else {
        var tbodyText = "";
        for (var i = 0; i < data["value"].length; i++) {
            tbodyText += "<tr>";
            for (var j = 0; j < data["value"][i].length; j++) {
                var value = data["value"][i][j];
                tbodyText += "<td>" + value + "</td>";
            }
            tbodyText += "</tr>";
        }
        $("#monitortable_tbody").html(tbodyText);
    }
    $("#dataTable").DataTable({
       "destroy": true
    });
}
