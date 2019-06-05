function CreateChartFunc(_chart_ip, _chart_type,data) {
    $("#chart_title").html("<i class='fa fa-yelp'></i><strong>&nbsp;" + _chart_type.toUpperCase() +
        "</strong>&nbsp;Charts For &nbsp;<strong>" + _chart_ip + "</strong>" );
    if ( _chart_type === "cpu" ) {
        cpuEchartsFunc("pic_1", data["loadval"]["title"],data["loadval"]["xaxis"], data["loadval"]["yaxis"], data["loadval"]["legend"]);
        cpuEchartsFunc("pic_2", data["cpuval"]["title"],data["cpuval"]["xaxis"], data["cpuval"]["yaxis"], data["cpuval"]["legend"]);
    } else if ( _chart_type === "memory" ) {
        memChartsFunc("pic_1",data);
    }
}

function cpuEchartsFunc(div_id,pic_title,pic_xaxis,pic_yaxis,pic_legendArr){
    var seriesArr = [];
    for (var L=0; L<pic_legendArr.length; L++ ) {
        var Arrdata = pic_yaxis[L];
        seriesArr.push({
            name: pic_legendArr[L],
            type: 'line',
            data: Arrdata,
            markPoint:{
                data: [{ type: 'max', name: 'max' }]      // 折线最大值显示标记点
            },
            itemStyle:{ normal:{ lineStyle:{ width: 3 } } },
            symbolSize: 5                                 // 拐角点大小
        })
    }
    var cpuChartOpts = {
        title: {
            text:pic_title
        },
        tooltip: { trigger: 'axis' },                      // 轴对齐时展示所有点信息
        legend: {
            data: pic_legendArr,                           // y轴线的标签信息 **需要填充数据
            textStyle: { fontSize: 16 }
        },
        grid: {                                            // 调整图形相对位置
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
            handleStyle: { color: '#fff', shadowBlur: 3, shadowColor: 'rgba(0, 0, 0, 0.6)', shadowOffsetX: 2, shadowOffsetY: 2 },
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
            axisLabel:{ textStyle:{ fontSize: 14 } }
        },
        yAxis: {                                           // y轴设置
            type: 'value',
            axisLabel:{ textStyle:{ fontSize: 14 } }
        },
        series: seriesArr                                  // 设置数据轴情况和样式  ***需要循环填入数据
    };
    var cpuChart = echarts.init(document.getElementById(div_id));
    cpuChart.setOption(cpuChartOpts,true);
    window.addEventListener("resize",function() {
        cpuChart.resize();
    });
}


function memChartsFunc(div_id,data) {
    var dataSetMem = [];
    for (var M in data["Memval"]["axis"]) {
        if (data["Memval"]["axis"].hasOwnProperty(M) ) {
            dataSetMem.push(data["Memval"]["axis"][M]);
        }
    }
    var dataSetmem = [];
    for (var m in data["memval"]["axis"]) {
        if (data["memval"]["axis"].hasOwnProperty(m) ) {
            dataSetmem.push(data["memval"]["axis"][m]);
        }
    }
    var memOpts = {
        legend: {},
        tooltip: { trigger: 'axis', showContent: false },
        dataset: [{
            dimension: data["memval"]["legend"],
            source: dataSetmem
        }, {
            dimension: data["Memval"]["legend"],
            source: dataSetMem
        }],
        xAxis: {type: 'category'},
        yAxis: {gridIndex: 0},
        grid: {top: '10%', left:'8%', right:'30%'},
        series: [
            {type: 'line', smooth: true,},
            {type: 'line', smooth: true,},
            {type: 'line', smooth: true,},
            {type: 'line', smooth: true,},
            {
                datasetIndex:0,
                type: 'pie',
                id: 'pie',
                radius: [0,'30%'],
                center: ['80%', '50%'],
                label:{},
                encode: {
                    value: 2,tooltip: 2
                },
                seriesLayoutBy: 'row'
            },{
                datasetIndex:1,
                type: 'pie',
                id: 'circle',
                radius: ['40%', '50%'],
                center: ['80%', '50%'],
                label:{},
                encode: {
                    value: 2,tooltip: 2
                },
                seriesLayoutBy: 'row'
            }
        ]
    };
    var memChart = echarts.init(document.getElementById("pic_1"));
    memChart.on('updateAxisPointer', function (event) {
        var xAxisInfo = event.axesInfo[0];
        if (xAxisInfo) {
            var dimension = xAxisInfo.value + 1;
            memChart.setOption({
                series: {
                    id: 'pie',
                    label: {},
                    encode: {
                        value: dimension,
                        tooltip: dimension
                    },
                }
            });
        }
    });
    var emptyChart = echarts.init(document.getElementById("pic_2"));
    emptyChart.clear();
    memChart.setOption(memOpts,true);
    window.addEventListener("resize",function() {
        memChart.resize();
    });
}