$("#monitordata_cpu").click(function() {
    CreateTableFunc();
    $.ajax({
        url: '/monitor/c',
        type: 'POST',
        dataType: 'json',
        data: {'type':"cpu",'option':"percent"},
        success: DataFunc
    });
});
$("#monitordata_memory").click(function(){
     CreateTableFunc();
     $.ajax({
         url: '/monitor/m',
         type: 'POST',
         dataType: 'json',
         data: {'type':"memory",'option':"GB"},
         success: DataFunc
     });
});
$("#monitordata_disk").click(function(){
     CreateTableFunc();
     $.ajax({
         url: '/monitor/d',
         type: 'POST',
         dataType: 'json',
         data: {'type':"disk"},
         success: DataFunc
     });
});
$("#monitordata_network").click(function(){
     CreateTableFunc();
     $.ajax({
         url: '/monitor/n',
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
        cardText += '<div class="card-header navbar"></div>';
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
    titleText += '<div><i class="fa fa-table"></i>'+ "\n" + data["title"] +'</div>';
    $(".card-header").html(titleText);
    var theadText = "";
    theadText += "<tr>";
    for (var a = 0; a < data["head"].length; a++) {
        var title = data["head"][a];
        theadText += "<td>" + title + "</td>";
    }
    theadText += "</tr>";
    $("#monitortable_thead").html(theadText);
    if ( data["title"] === "Disk List") {
        var diskText = "";
        for (var x=0; x< data["value"].length; x++) {
            var arr = JSON.parse(data["value"][x][2]);
            for (var y=0; y< data["value"][x][1].length; y++) {
                diskText += "<tr>";
                diskText += "<td>" + data["value"][x][1][y] + "</td>";
                diskText += "<td><ul>";
                diskText += "<li>" + "Used:" + arr[y].used + "GB" + "</li>";
                diskText += "<li>" + "Total:" + arr[y].total + "GB" + "</li>";
                diskText += "<li>" + "Percent:" + arr[y].percent + "%" + "</li>";
                diskText += "<li>" + "Inode:" + arr[y].inode + "%" + "</li>";
                diskText += "</ul></td></tr>";
            }
        }
        $("#monitortable_tbody").html(diskText);
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
    // $("#dataTable").DataTable({
    //     "destroy": true
    // });
}
