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
            cardText += '<thead id="monitortable_thead"><thead>';
            cardText += '<tbody id="monitortable_tbody"></tbody>';
            cardText += '</table></div></div></div>';
            $("#mainSubweb").html(cardText);
        }
    }
    function DataFunc(data) {
        var titleText = "";
        titleText += '<div><i class="fa fa-table"></i>'+ "\n" + data["title"] +'</div>';
        $(".card-header").html(titleText);
        var theadText = "";
        theadText += "<tr>" + "\n";
        for (var x = 0; x<data["head"].length; x++) {
            var title = data["head"][x];
            theadText += "<td>" + title + "</td>" + "\n";
        }
        theadText += "</tr>";
        var tbodyText = "";
        for (var i = 0; i < data["value"].length; i++) {
            tbodyText += "<tr>" + "\n";
            for (var j = 0; j < data["value"][i].length; j++) {
                var value = data["value"][i][j];
                tbodyText += "<td>" + value + "</td>" + "\n";
            }
            tbodyText += "</tr>";
        }
        $("#monitortable_thead").html(theadText);
        // $("#monitortable_tbody").html(tbodyText);
        // $("#dataTable").DataTable({
        //    "destroy": true
        // });
    }
