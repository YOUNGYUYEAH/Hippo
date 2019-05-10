// 切换表格的时候出现格式异常
$("#monitordata_cpu").click(function() {
    CreateTableFunc();
    $.ajax({
        url: '/monitor/c',
        type: 'POST',
        dataType: 'json',
        data: {'option':"percent"},
        success: DataFunc
    });
});
$("#monitordata_memory").click(function(){
     CreateTableFunc();
     $.ajax({
         url: '/monitor/m',
         type: 'POST',
         dataType: 'json',
         data: {'option':"GB"},
         success: DataFunc
     });
});
    function CreateTableFunc() {
        if ($("#card-table").length > 0) {
            console.log("find card-table");
        } else {
            var cardText = "";
            cardText += '<div class="card mb-8">';
            cardText += '<div class="card-body">';
            cardText += '<div class="table-responsive">';
            cardText += '<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">';
            cardText += '<thead id="monitortable_thead"><thead>';
            cardText += '<tbody id="monitortable_tbody"></tbody>';
            cardText += '</table></div></div></div>';
            $("#mainSubweb").html(cardText);

            // var carddiv = $('<div></div>');
            // carddiv.addClass("card mb-8").attr('id',"card-table");
            // $("#mainSubweb").append(carddiv);
            // var cardbodydiv = $('<div></div>');
            // cardbodydiv.addClass("card-body").appendTo(carddiv);
            // var cardtablediv = $('<div></div>');
            // cardtablediv.addClass("table-responsive").appendTo(cardbodydiv);
            // var tablediv = $('<table></table>');
            // tablediv.addClass("table table-bordered").attr({'id':"dataTable","width":"100%","cellspacing":"0"}).appendTo(cardtablediv);
            // var theaddiv = $('<thead></thead>');
            // var tbodydiv = $('<tbody></tbody>');
            // theaddiv.attr('id',"monitortable_thead").appendTo(tablediv);
            // tbodydiv.attr('id',"monitortable_tbody").appendTo(tablediv);
        }
    }
    function DataFunc(data) {
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
        $("#monitortable_tbody").html(tbodyText);
        $("#dataTable").DataTable({
            "destroy": true
        });
    }
