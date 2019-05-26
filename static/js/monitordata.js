function TransBitFunc(number,basenum,fixednum,unit) {
    /* 将数字转换为进制数,且保留小数的函数,再根据单位进行换算 */
    var num;
    if ( unit === "%" ) {
        if ( number !== 0 ) {
            num = number + "%";
        } else {
            num = number;
        }
    } else if( number > Math.pow(basenum,3) ) {
        if ( unit === "bit") {
            num = ( number/(Math.pow(basenum,3)) ).toFixed(fixednum) + "GB";
        } else if ( unit === "b/s" ) {
            num = ( number/(Math.pow(basenum,3)) ).toFixed(fixednum) + "Gb/s";
        }
    } else if ( number > Math.pow(basenum,2) ) {
        if ( unit === "bit") {
            num = ( number/(Math.pow(basenum,2)) ).toFixed(fixednum) + "MB";
        } else if ( unit === "b/s" ) {
            num = ( number/(Math.pow(basenum,2)) ).toFixed(fixednum) + "Mb/s";
        }
    } else if ( number > basenum ) {
        if ( unit === "bit" ) {
            num = ( number/basenum ).toFixed(fixednum) + "KB";
        } else if (unit === "b/s" ) {
            num = ( number/basenum ).toFixed(fixednum) + "Kb/s";
        }
    } else if ( number !== 0 ) {
        if ( unit === "bit" ) {
            num = number + "bit";
        } else if ( unit === "b/s" ) {
            num = number + "b/s";
        }
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
        cardText += '<thead id="monitortable_thead" class="info_title">';
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
    titleText += "<div><i class='fa fa-table'></i>" + "&nbsp;" + data["title"] + "</div>";
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
                diskText += "<li>" + "Used: " + TransBitFunc(arr[z]["used"],1024,2,"bit") + "</li>";
                diskText += "<li>" + "Total: " + TransBitFunc(arr[z]["total"],1024,2,"bit") + "</li>";
                diskText += "<li>" + "Percent: " + TransBitFunc(arr[z]["percent"],1,1,"%") + "</li>";
                diskText += "<li>" + "Inode: " + TransBitFunc(arr[z]["inode"],1,1,"%") + "</li>";
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
                        netText += "<li><a class='table-a-fix'>" + TransBitFunc(item[v1],1024,2,"b/s")
                            + "</a></li><li><a>" + TransBitFunc(item[v2],1024,2,"b/s") + "</a></li>";
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
                    tbodyText += "<td>" + TransBitFunc(value,1024,2,"bit") + "</td>";
                } else if ((data["title"] === "CPU List") && (( j>4 ) && ( j< data["value"][i].length-1 ))) {
                    tbodyText += "<td>" + TransBitFunc(value,1,1,"%") + "</td>";
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

function InfoFunc(name,data,data_index,infoObj,is_append) {
    var searchinfoText = "";
    var _headText = "";
    var _bodyText = "";
    var _count = "";
    infoObj = JSON.parse(infoObj);
    if ( name !== "Disk" && name !== "Network" ) {
        _headText += "<tr>";
        if ( is_append === 1) {
            _bodyText += "<tr class='comparison_tr'>";
        } else {
            _bodyText += "<tr class='reference_tr'>";
        }
        $.each(infoObj, function (infoObj_idx, infoObj_item) {
            if ( infoObj_idx === "Load" ) {
                _count += 2;
                _headText += "<td colspan='3' style='text-align:center'>" + infoObj_idx + " [1min 5min 15min]" + "</td>";
                _bodyText += "<td>" + data["value"][data_index]["load_1"] + "</td>";
                _bodyText += "<td>" + data["value"][data_index]["load_5"] + "</td>";
                _bodyText += "<td>" + data["value"][data_index]["load_15"] + "</td>";
            } else {
                _headText += "<td>" + infoObj_idx + "</td>";
                if ( name === "CPU" && infoObj_idx !== "Count" ) {
                    _bodyText += "<td>" + TransBitFunc(data["value"][data_index][infoObj_item],1,1,"%") + "</td>";
                } else if ( name === "Memory" ) {
                    _bodyText += "<td>" + TransBitFunc(data["value"][data_index][infoObj_item],1024,2,"bit") + "</td>";
                } else {
                    _bodyText += "<td>" + data["value"][data_index][infoObj_item] + "</td>";
                }
            }
            _count++;
        });
        _bodyText += "</tr>";
        _headText += "</tr>";
    } else {
        _headText += "<tr>";
        $.each(infoObj,function (infoObj_key,infoObj_val) {
            _count ++;
            _headText += "<td>" + infoObj_key + "</td>";
        });
        _headText += "</tr>";
        if ( name === "Disk" ) {
            var PartArr = data["value"][data_index]["diskmount"].split("[")[1].split("]")[0].split(",");
            var ValueArr = data["value"][data_index]["diskusage"].split("['")[1].split("']")[0].split("', '");
            for ( var Len=0; Len < PartArr.length; Len++ ) {
                if ( is_append === 1) {
                    _bodyText += "<tr class='comparison_tr'>";
                } else {
                    _bodyText += "<tr class='reference_tr'>";
                }
                _bodyText += "<td>" + PartArr[Len] + "</td>";
                var ValueJArr = JSON.parse(ValueArr[Len]);
                for ( var Arrval in infoObj ) {
                    if ( infoObj.hasOwnProperty(Arrval)) {
                        if (Arrval !== "Mount") {
                            if (Arrval !== "Percent" && Arrval !== "Inode") {
                                _bodyText += "<td>" + TransBitFunc(ValueJArr[infoObj[Arrval]],1024,2,"bit") + "</td>";
                            } else {
                                _bodyText += "<td>" + TransBitFunc(ValueJArr[infoObj[Arrval]],1,1,"%") + "</td>";
                            }
                        }
                    }
                }
                _bodyText += "</tr>";
            }
        } else if ( name === "Network" ) {
            var PicArr = data["value"][data_index]["netpic"].split("[")[1].split("]")[0].split(",");
            var netArr = data["value"][data_index]["netusage"].split("['")[1].split("']")[0].split("', '");
            for ( var len=0; len < PicArr.length; len++ ) {
                if ( is_append === 1) {
                    _bodyText += "<tr class='comparison_tr'>";
                } else {
                    _bodyText += "<tr class='reference_tr'>";
                }
                _bodyText += "<td>" + PicArr[len] + "</td>";
                var netJArr = JSON.parse(netArr[len]);
                for ( var netval in infoObj ) {
                    if ( infoObj.hasOwnProperty(netval) ) {
                        if ( netval !== "Interface" ) {
                            if (netval !== "Speed" && netval !== "Interface" && netval !== "IPaddr") {
                                _bodyText += "<td>" + TransBitFunc(netJArr[infoObj[netval]], 1024, 2, "b/s") + "</td>";
                            } else {
                                _bodyText += "<td>" + netJArr[infoObj[netval]] + "</td>";
                            }
                        }
                    }
                }
                _bodyText += "</tr>";
            }
        }
    }
    searchinfoText += "<thead id='" + name + "_head'><tr><td class='search_title' colspan='"
        + _count + "'>" + name + "</td></tr></thead>";
    searchinfoText += "<tbody id='" + name + "_body'></tbody>";
    if ( is_append === 1 ){
        $("#" + name + "_body").append(_bodyText);
    } else {
        $("#" + name).html(searchinfoText);
        $("#" + name + "_head").append(_headText);
        $("#" + name + "_body").html(_bodyText);
    }
    $("#search_info").show();
}

function SearchFunc(opts_val,opts2_text,is_comparison) {
    $.ajax({
        url: '/monitor/s',
        type: 'POST',
        cache: false,
        data: {'type': "host", 'option': opts_val},
        success: function (data, statusText, xhr) {
            if ( xhr.status === 200 ) {
                var search_title = "";
                if ( is_comparison === 0 ) {
                    search_title = "<i class='fa fa-yelp'></i>" + "&nbsp; Information For &nbsp;"
                        + "<strong>" + opts2_text + "</strong> &nbsp; At &nbsp; <strong>"
                        + data["value"][1]["checktime"] + "</strong>";
                    $("#search_info_title").html(search_title);
                } else if ( is_comparison === 1) {
                    search_title = "<i class='fa fa-yelp'></i>" + "&nbsp; Comparison &nbsp;" + "<strong>"
                        + $("#search_info_title strong:first").text() + "</strong>" + "&nbsp; And &nbsp;"
                        + "<strong>" + opts2_text + "</strong>";
                    $("#comparison_title").html(search_title).removeAttr("hidden");
                    $("#search_info_title").attr("hidden","hidden");
                }
                for (var T=0; T<data["title"].length; T++) {
                    InfoFunc(data["title"][T], data, T, data["index"][data["title"][T]],is_comparison);
                }
            } else {
                alert(data["error"]);
            }
        }
    });
}

/* 按钮点击后执行对应功能 */
$("#showlist_btn").click(function(){
    /* 列表展示按钮,屏蔽某IP详情,展示列表数据 */
    $(this).attr("hidden","hidden");
    $("#charts_btn").attr("hidden","hidden");
    $("#comparison_btn").attr("hidden","hidden");
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
        $("#comparison_btn").removeAttr("hidden");
        SearchFunc(search_host.val(), search_host.text(),0)
    }
    $("#comparison_btn").attr("value","Compare").html("<i class='fa fa-files-o'>&nbsp;Compare</i>");
    $("#comparison_title").attr("hidden","hidden");
    $("#search_info_title").removeAttr("hidden","hidden");
});
$("#comparison_btn").click(function(){
    if ( $(this).val() === "Compare" ) {
        var reference_ip = $("#search_info_title strong:first").text();
        var compare_ip = $("#select_host_ip").find("option:selected").text();
        if (reference_ip === compare_ip) {
            // alert("Please Choose Different IP.");
        } else {
            var new_select = $("#select_host_ip").find("option:selected");
            SearchFunc(new_select.val(), new_select.text(), 1);
            $("#comparison_btn").attr("value", "Uncompare").html(
                "<i class='fa fa-files-o'></i>&nbsp;Uncompare");
            $("#charts_btn").attr("hidden","hidden");
        }
    } else if ( $(this).val() === "Uncompare" ) {
        $(".comparison_tr").remove();
        $("#comparison_btn").attr("value","Compare").html(
            "<i class='fa fa-files-o'></i>&nbsp;Compare");
        $("#search_info_title").removeAttr("hidden");
        $("#comparison_title").empty().attr("hidden","hidden");
        $("#charts_btn").removeAttr("hidden");
    }
});

