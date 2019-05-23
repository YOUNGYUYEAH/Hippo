$(document).ready(function(){
    /* 1.页面初始加载为下拉框添加一个隐藏默认值(火狐浏览器有异常); 2.执行LoadWebFunc加载server列表; 3.屏蔽查询结果的卡片显示栏 */
    {
        var sss = $("#select_host_ip");
        if ( sss.length > 0 ) {
            sss.find("option:selected").removeAttr("selected");
            var selectText = "";
            selectText += "<option data-hidden='true' disabled='disabled' selected='selected'> "
                + "Select Server To Search :D" + "</option>" ;
            sss.append(selectText);
        }
        LoadWebFunc("server");
        $("#search_info").hide();
    }
});

function TransBitFunc(number,basenum,fixednum) {
    /* 将数字转换为进制数,且保留小数的函数 */
    var num;
    if(number > Math.pow(basenum,3)) {
        num = (number/(Math.pow(basenum,3))).toFixed(fixednum) + "GB";
    } else if (number > Math.pow(basenum,2)) {
        num = (number/(Math.pow(basenum,2))).toFixed(fixednum) + "MB";
    } else if (number > basenum) {
        num = (number/basenum).toFixed(fixednum) + "KB"
    } else {
        num = number;
    } return num;
}

function CreateTableFunc() {
    /* 创建一个card->table用于加载AJAX传回的数据 */
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

function LoadWebFunc(search_type) {
    /* AJAX向后台请求对应的值,成功后拼接数据,组成页面 */
    if ( search_type !== "server") {
        CreateTableFunc();
    }
    $.ajax({
        url: '/monitor/s',
        type: 'POST',
        dataType: 'json',
        data: {'type':search_type},
        success: DataFunc
    });
}

function DataFunc(data) {
    /* 从后台获取的数据进行table的拼接和数据渲染,配合dataTable插件完成表格 */
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
                diskText += "<li>" + "Used: " + arr[z]["used"] + "GB" + "</li>";
                diskText += "<li>" + "Total: " +arr[z]["total"] + "GB" + "</li>";
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
            function _netvalue(v1,v2) {
                netText += "<td><ul class='table-ul'>";
                $.each(Arr, function (index, item) {
                    if(!v2) {
                        netText += "<li>" + item[v1] + "</li>";
                    } else {
                        netText += "<li><span class='table-span'>" + item[v1] + "</span><span class='table-span'>" + item[v2] + "</span></li>";
                    }
                    if (index !== Arr.length - 1) {
                        netText += "<hr class='table-hr' />";
                    }
                });
                netText += "</ul></td>";
            }
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
                if (( data["title"] === "Memory List") && (( j !== 0 ) && ( j !== data["value"][i].length-1 ))) {
                    tbodyText += "<td>" + TransBitFunc(value,1024,2) + "</td>";
                } else if ((data["title"] === "CPU List") && (( j>4 ) && ( j< data["value"][i].length-1 ))) {
                    if (value !== 0) {
                        tbodyText += "<td>" + value + "%" + "</td>";
                    } else {
                        tbodyText += "<td>" + value + "</td>";
                    }
                } else {
                    tbodyText += "<td>" + value + "</td>";
                }
            }
            tbodyText += "</tr>";
        }
        $("#monitortable_tbody").html(tbodyText);
    }
    $("#dataTable").DataTable({
       "destroy": true
    });
}

/* 几个tab标签点击后执行对应功能 */
$("#monitordata_server").click(function() { window.location.reload(); });
$("#monitordata_cpu").click(function(){ LoadWebFunc("cpu");});
$("#monitordata_disk").click(function() { LoadWebFunc("disk");});
$("#monitordata_memory").click(function() { LoadWebFunc("memory");});
$("#monitordata_network").click(function() { LoadWebFunc("network");});

/* 按钮点击后执行对应功能 */
$("#showlist_btn").click(function(){
    /* 列表展示按钮,屏蔽某IP详情,展示列表数据 */
    $(this).attr("hidden","hidden");
    $("#charts_btn").attr("hidden","hidden");
    $("#search_info").hide();
    $("#server_card").show();
});
$("#hostmode_btn").click(function(){
    /* 查询按钮,显示被选中的IP的详情页,屏蔽列表数据 */
    var search_host =  $("#select_host_ip").find("option:selected");
    if ( ! search_host.prop("disabled") && search_host.val() !== "" ) {
        $("#server_card").hide();
        $("#showlist_btn").removeAttr("hidden");
        $("#charts_btn").removeAttr("hidden");
        var search_title = "<i class='fa fa-yelp'></i>" + "&nbsp Information For &nbsp" + "<strong>"
            + search_host.text() + "</strong>";
        $("#search_info_title").html(search_title);
        $.ajax({
            url: '/monitor/s',
            type: 'POST',
            cache: false,
            data: {'type': "host", 'option': search_host.val()},
            success: function (data, statusText, xhr) {
                if ( xhr.status === 200 ) {
                    InfoFunc(data);
                } else {
                    alert(data["error"]);
                }
            }
        });
    }
});

function InfoFunc(data) {
    // alert(data["value"]);
    for (var S=0; S<data["value"].length; S++) {
        var msgText = "";
        $.each(data["value"][S], function (i_idx, i_item) {
            msgText += "<dl>";
            msgText += "<dt class='dl-float'>" + i_idx + "</dt>";
            msgText += "<dd>" + i_item + "</dd>";
            msgText += "</dl>";
        });
        $("#"+data["title"][S]).html(msgText);
    }
    $("#search_info").show();
}





//$("#hostmode_btn").click(function(){
//    var search_host =  $("#select_host_ip").find("option:selected");
//    if ( ! search_host.prop("disabled") && search_host.val() !== "" ) {
//        $("#server_card").hide();
//        $("#showlist_btn").removeAttr("hidden");
//        $("#charts_btn").removeAttr("hidden");
//        var search_title = "<i class='fa fa-yelp'></i>" + "&nbsp Information For &nbsp" + "<strong>"
//            + search_host.text() + "</strong>";
//        $.ajax({
//            url: '/monitor/s',
//            type: 'POST',
//            cache: false,
//            data: {'type':"host", 'option': search_host.val()},
//            success: function(data,statusText,xhr){
//                if ( xhr.status === 200 ) {
//                    $("#search_info_title").html(search_title);
//                    function Objdata(index,tid) {
//                        var Value = "";
//                        Value += "<thead><tr>";
//                        for (var key in data["value"][index]) {
//                            Value += "<td><strong>" + key + "</strong></td>";
//                        }
//                        Value += "</tr></thead><tbody><tr>";
//                        if (( tid !== 'disk' ) && ( tid !== 'network')) {
//                            $.each(data["value"][index], function (idx, item) {
//                                if (index === "2") {
//                                    if (idx === "checktime") {
//                                        Value += "<td>" + item + "</td>";
//                                    } else {
//                                        Value += "<td>" + TransBitFunc(item,1024,2) + "</td>";
//                                    }
//                                } else {
//                                    Value += "<td>" + item + "</td>";
//                                }
//                            });
//                        } else {
//                            $.each(data["value"][index], function (IDX,ITEM) {
//                                Value += "<td><ul class='table-ul'>";
//                                if (IDX !== "checktime") {
//                                    if (IDX === "diskmount" || IDX === "netpic" ) {
//                                        var _value_arr = ITEM.split("[")[1].split("]")[0].split(",");
//                                        for (var W = 0; W < _value_arr.length; W++) {
//                                            Value += "<li>" + _value_arr[W] + "</li>";
//                                            if (W !== _value_arr.length - 1) {
//                                                Value += "<hr class='table-hr' />";
//                                            }
//                                        }
//                                    } else if (IDX === "diskusage" || IDX === "netusage") {
//                                        var _usage_arr = ITEM.split("['")[1].split("']")[0].split("', '");
//                                        for (var G=0; G<_usage_arr.length; G++) {
//                                            var _usage_jsonarr = JSON.parse(_usage_arr[G]);
//                                            Value += "<li><nav class='table-nav'>";
//                                            if( IDX === "diskusage" ) {
//                                                Value += "<a>" + "Used: " + _usage_jsonarr["used"] +"</a>";
//                                                Value += "<a>" + "Total: " + _usage_jsonarr["total"] +"</a>";
//                                                Value += "<a>" + "Percent: " + _usage_jsonarr["percent"] +"</a>";
//                                                Value += "<a>" + "Inode:" + _usage_jsonarr["inode"] +"</a>";
//                                            } else if (IDX === "netusage") {
//                                                Value += "<a>" + "Netaddr: " + _usage_jsonarr["ipaddr"] +"</a>";
//                                                Value += "<a>" + "Speed: " + _usage_jsonarr["speed"] +"</a>";
//                                                Value += "<a>" + "Bps_Sent[1s]: " + _usage_jsonarr["bps_sent"] +"</a>";
//                                                Value += "<a>" + "Bps_Recv[1s]: " + _usage_jsonarr["bps_recv"] +"</a>";
//                                                Value += "<a>" + "Pps_Sent[1s]: " + _usage_jsonarr["pps_sent"] +"</a>";
//                                                Value += "<a>" + "Pps_Recv[1s]: " + _usage_jsonarr["pps_recv"] +"</a>";
//
//                                            }
//                                            if ( G !== _usage_arr.length -1 ) {
//                                                Value += "<hr class='table-hr' />";
//                                            }
//                                            Value += "</nav></li>";
//                                        }
//                                    }
//                                } else {
//                                    var _value = ITEM;
//                                    Value += "<li>" + _value + "</li>";
//                                }
//                                Value += "</ul></td>";
//                            })
//                        }
//                        Value += "</tr></tbody>";
//                        $("#"+tid).html(Value);
//                    }
//                    Objdata("0", "info");
//                    Objdata("1", "cpu");
//                    Objdata("2", "memory");
//                    Objdata("3", "disk");
//                    Objdata("4", "network");
//                    $("#search_info").show();
//                } else if ( xhr.status === 500 ) {
//                    alert(data["error"]);
//                }
//            }
//        });
//    }
//});
