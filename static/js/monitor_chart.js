function CreateChartFunc(_chart_ip, _chart_type,data) {
    $("#chart_title").html("<i class='fa fa-yelp'></i><strong>&nbsp;" + _chart_type.toUpperCase() +
        "</strong>&nbsp;Charts For &nbsp;<strong>" + _chart_ip + "</strong>" );
    EchartsFunc("pic_1",data["loadval"]["xaxis"],data["loadval"]["yaxis"],data["loadval"]["legend"],"Line");
}

function EchartsFunc(div_id,pic_xaxis,pic_yaxis,pic_legendArr,chart_type){
    // var pic_legendArr = pic_legend.split(",");
    if ( chart_type === "Line" ) {
        var seriesArr = [];
        for (var L=0; L<pic_legendArr.length; L++ ) {
            var Arrdata = pic_yaxis[L].split(",");
            seriesArr.push({
                name: pic_legendArr[L],
                type: 'line',
                data: Arrdata,
                itemStyle:{
                    normal:{
                        lineStyle:{
                            width: 3                           // 线粗细程度
                        },
                    }
                },
                symbolSize: 10                                 // 拐角点大小
            })
        }
        var LineChartOpts = {
            backgroundColor: '#f7f7f7',
            tooltip: { trigger: 'axis' },                      // 轴对齐时展示所有点信息
            legend: {
                data: pic_legendArr,                           // y轴线的标签信息 **需要填充数据
                textStyle: {
                    fontSize: 16                               // 标识信息字体大小
                }
            },
            grid: {                                            // 调整图形相对位置
                top:'10%',
                left: '3%',
                bottom: '8%',
                right: '3%',
                containLabel:true
            },
            dataZoom: {                                        // 设置区域放大滑动轴
                id: 'dataZoomX',
                type: 'slider',
                xAxisIndex:[0],
                filterMode:'filter'
            },
            toolbox: {                                         // 工具箱设置
                orient: 'horizontal',
                x: '90%',
                feature: {
                    saveAsImage:{},                            // 添加保存为图片的工具栏
                    restore:{}
                }
            },
            xAxis: {                                           // x轴设置
                type: 'category',
                boundaryGap: false,                            // x轴数据点为点状,非面积[这个设置能使图线贴y轴]
                data: pic_xaxis,                               // **需要填充数据
                axisLabel:{
                    textStyle:{
                        fontSize: 14
                    }
                }
            },
            yAxis: {                                           // y轴设置
                type: 'value',
                axisLabel:{
                    textStyle:{
                        fontSize: 14
                    }
                }
            },
            series: seriesArr                                  // 设置数据轴情况和样式  ***需要循环填入数据
        };
        echarts.init(document.getElementById(div_id)).setOption(LineChartOpts);
    }
}

$("#createchart_btn").click(function(){
    var create_chart_ip = $("#select_ip").find("option:selected");
    var _chart_host_ip = create_chart_ip.text();
    if ( ! create_chart_ip.prop("disabled") && create_chart_ip.val() !== "" ) {
        var _chart_ip = _chart_host_ip.split("(")[1].split(")")[0];
        var _chart_type = $("#select_chart_type").find("option:selected").val();
        $.ajax({
            url: '/monitor/c',
            type: 'POST',
            cache: false,
            data: {'ip': _chart_ip,
                'type':_chart_type,
                'time_start':"2019-05-27 08:00:00",
                'time_end':"2019-05-27 10:00:00"
            },
            success: function(data, statsText, xhr) {
                if ( xhr.status === 200) {
                    //alert(data["cputime"]);
                    CreateChartFunc(_chart_host_ip,_chart_type,data);
                    $("#Chartsweb").removeAttr("hidden");
                }
            },
        })
    }
});

