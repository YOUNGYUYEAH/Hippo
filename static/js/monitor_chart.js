$(document).ready(function() {
    $("#time_dropdown_main .dropdown-menu").click("[data-stopPropagtion]", function (e) {
        e.stopPropagation();
    });

    var today = new Date();
    var oneday = 1000 * 60 * 60 * 24;

    $("#begin_day_btn").click(function () {
        $("#begin_day").datepicker({
            format: 'yyyy-mm-dd',
            autoclose: true,
            orientation: 'bottom',
            startDate: new Date(today- oneday*14),
            endDate: new Date(),
        }).focus();
    });
    $("#end_day_btn").click(function () {
        $("#end_day").datepicker({
            format: 'yyyy-mm-dd',
            autoclose: true,
            orientation: 'bottom',
        }).focus();
    });

    function TimeClickFunc(_SetTime) {
        var maxNumber = _SetTime.find('input').attr("max");
        var minNumber = _SetTime.find('input').attr("min");
        _SetTime.find('.btn:first-of-type').click(function () {
            _SetTime.find("input").focus();
            if (parseInt(_SetTime.find('input').val()) >= minNumber && parseInt(_SetTime.find('input').val()) < 9) {
                _SetTime.find('input').attr('value', "0" + (parseInt(_SetTime.find('input').val(), 10) + 1));
            } else if ( parseInt(_SetTime.find('input').val()) >= 9 && parseInt(_SetTime.find('input').val()) < maxNumber) {
                _SetTime.find('input').attr('value',parseInt(_SetTime.find('input').val(), 10) + 1);
            } else {
                _SetTime.find('input').attr('value',"0"+minNumber);
            }
        });
        _SetTime.find('.btn:last-of-type').click(function () {
            _SetTime.find("input").focus();
            if (parseInt(_SetTime.find('input').val()) > minNumber && parseInt(_SetTime.find('input').val()) <= 10) {
                _SetTime.find('input').attr('value',"0" + (parseInt(_SetTime.find('input').val(), 10) - 1));
            } else if (parseInt(_SetTime.find('input').val()) > 9 && parseInt(_SetTime.find('input').val()) <= maxNumber) {
                _SetTime.find('input').attr('value', parseInt(_SetTime.find('input').val(), 10) - 1);
            } else {
                _SetTime.find('input').attr('value',maxNumber);
            }
        });
    }
    TimeClickFunc($("#begin_hour"));
    TimeClickFunc($("#begin_minute"));
    TimeClickFunc($("#end_hour"));
    TimeClickFunc($("#end_minute"));
});

function ChangeDateTimeFunc() {

}

function CreateChartFunc(_chart_ip, _chart_type,data) {
    $("#chart_title").html("<i class='fa fa-yelp'></i><strong>&nbsp;" + _chart_type.toUpperCase() +
        "</strong>&nbsp;Charts For &nbsp;<strong>" + _chart_ip + "</strong>" );
    if ( _chart_type === "cpu" ) {
        EchartsFunc("pic_1", data["loadval"]["xaxis"], data["loadval"]["yaxis"], data["loadval"]["legend"], "Line");
        EchartsFunc("pic_2", data["cpuval"]["xaxis"], data["cpuval"]["yaxis"], data["cpuval"]["legend"], "Line");
    } else if ( _chart_type === "memory" ) {
        EchartsFunc("pic_1","","","","Pie");
    }
}

function EchartsFunc(div_id,pic_xaxis,pic_yaxis,pic_legendArr,chart_type){
    // var pic_legendArr = pic_legend.split(",");
    if ( chart_type === "Line" || chart_type === "Bar" ) {
        var seriesArr = [];
        for (var L=0; L<pic_legendArr.length; L++ ) {
            var Arrdata = pic_yaxis[L];
            seriesArr.push({
                name: pic_legendArr[L],
                type: chart_type.toLowerCase(),
                data: Arrdata,
                markPoint:{
                    data: [{ type: 'max', name: 'max' }]      // 折线最大值显示标记点
                },
                itemStyle:{
                    normal:{
                        lineStyle:{
                            width: 3                          // 线粗细程度
                        },
                    }
                },
                symbolSize: 5                                 // 拐角点大小
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
            dataZoom: [{                                       // 设置区域放大滑动轴
                id: 'dataZoomX',
                type: 'slider',
                xAxisIndex:[0],
                filterMode:'filter',
            }, {                                               // 更换滑动条的触点样式
                handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-' +
                '1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z ' +
                'M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                handleSize: '80%',
                handleStyle: {
                    color: '#fff',
                    shadowBlur: 3,
                    shadowColor: 'rgba(0, 0, 0, 0.6)',
                    shadowOffsetX: 2,
                    shadowOffsetY: 2
                }
            }],
            toolbox: {                                         // 工具箱设置
                orient: 'horizontal',
                x: '90%',
                feature: {
                    saveAsImage:{},                            // 添加保存为图片的工具栏
                    restore:{},                                // 添加还原所有设置项的工具栏
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
    } else if ( chart_type === "Pie") {
        var PieChartOpts = {
            tooltip: {
                trigger:'item',
                formatter: "{a}</br>{b}:{c}({d}%)"
            },
            series: [
                {
                    name:'memory',
                    type:'pie',
                    radius: ['0', '40%'],
                    label: {
                        normal:{
                            position: 'inner'
                        }
                    },
                    labelLine: {
                        normal: {
                            show: false
                        }
                    },
                    data:[
                        { value:335, name:'测试1' },
                        { value:679, name:'测试2' },
                        { value:1548, name:'测试3' }
                    ]
                },{
                    name: 'memory',
                    type: 'pie',
                    selectedMode: 'single',
                    radius: ['50%','70%'],
                    label: {
                        normal: {
                            formatter: '{b|{b}：}{c}  {per|{d}%}  ',
                            rich: {
                                b: {
                                    fontSize: 16,
                                    lineHeight: 33
                                },
                                per: {
                                    color: '#eee',
                                    backgroundColor: '#334455',
                                    padding: [2, 4],
                                    borderRadius: 2
                                }
                            }
                        }
                    },
                    data:[
                        {value:335, name:'测试1', selected:true},
                        {value:310, name:'测试2-1'},
                        {value:234, name:'测试2-2'},
                        {value:135, name:'测试2-3'},
                        {value:1048, name:'测试3-1'},
                        {value:251, name:'测试3-2'},
                        {value:147, name:'测试3-3'},
                        {value:102, name:'测试3-4'}
                    ]
                }
            ]
        };
        echarts.init(document.getElementById(div_id)).setOption(PieChartOpts);
    }
}

$("#createchart_btn").click(function(){
    var create_chart_ip = $("#select_ip").find("option:selected");
    var _chart_host_ip = create_chart_ip.text();
    var time_range = $("#select_time").val();
    if ( ! create_chart_ip.prop("disabled") && create_chart_ip.val() !== "" ) {
        var _chart_ip = _chart_host_ip.split("(")[1].split(")")[0];
        var _chart_type = $("#select_type").find("option:selected").val();
        $.ajax({
            url: '/monitor/c',
            type: 'POST',
            cache: false,
            data: {'ip': _chart_ip,
                'type':_chart_type,
                'time_range': time_range
            },
            success: function(data, statsText, xhr) {
                if ( xhr.status === 200) {
                    CreateChartFunc(_chart_host_ip,_chart_type,data);
                    $("#Chartsweb").removeAttr("hidden");
                }
            },
        })
    }
});

$("#begin_minute input").focus(function(){
    var _btm = $("#begin_minute input").val();
    var _ns = new Date().getSeconds();
    if (_ns < 10 ) {
        _ns = "0" + _ns;
    }
    var new_timerange = $("#begin_day").val() + " " + $("#begin_hour input").val() + ":" + _btm + ":" + _ns
        + " - " + $("#end_day").val() + " " + $("#end_hour input").val() + ":" + $("#end_minute input").val() + ":" + _ns;
    $("#select_time").attr("value",new_timerange)
});
$("#begin_hour input").focus(function(){
    var _bth = $("#begin_hour input").val();
    var _ns = new Date().getSeconds();
    if (_ns < 10 ) {
        _ns = "0" + _ns;
    }
    var new_timerange = $("#begin_day").val() + " " + _bth + ":" + $("#begin_minute input").val() + ":" + _ns
        + " - " + $("#end_day").val() + " " + $("#end_hour input").val() + ":" + $("#end_minute input").val() + ":" + _ns;
    $("#select_time").attr("value",new_timerange)
});
$("#end_minute input").focus(function(){
    var _etm = $("#end_minute input").val();
    var _ns = new Date().getSeconds();
    if (_ns < 10 ) {
        _ns = "0" + _ns;
    }
    var new_timerange = $("#begin_day").val() + " " + $("#begin_hour input").val() + ":" + $("#begin_minute input").val() + ":" + _ns
        + " - " + $("#end_day").val() + " " + $("#end_hour input").val() + ":" + _etm + ":" + _ns;
    $("#select_time").attr("value",new_timerange)
});
$("#end_hour input").focus(function(){
    var _eth = $("#end_hour input").val();
    var _ns = new Date().getSeconds();
    if (_ns < 10 ) {
        _ns = "0" + _ns;
    }
    var new_timerange = $("#begin_day").val() + " " + $("#begin_hour input").val() + ":" + $("#begin_minute input").val() + ":" + _ns
        + " - " + $("#end_day").val() + " " + _eth + ":" + $("#end_minute input").val() + ":" + _ns;
    $("#select_time").attr("value",new_timerange)
});