function CreateChartFunc(_chart_ip, _chart_type,data) {
    $("#chart_title").html("<i class='fa fa-yelp'></i><strong>&nbsp;" + _chart_type.toUpperCase() +
        "</strong>&nbsp;Charts For &nbsp;<strong>" + _chart_ip + "</strong>" );
    for (var Pic=0; Pic<6; Pic++) {
        $("#pic_"+Pic).attr("hidden","hidden");
    }
    if ( _chart_type === "cpu" ) {
        $("#pic_1").removeAttr("hidden");
        $("#pic_2").removeAttr("hidden");
        cpuEchartsFunc("pic_1", data["loadval"]["title"],data["loadval"]["xaxis"], data["loadval"]["yaxis"], data["loadval"]["legend"]);
        cpuEchartsFunc("pic_2", data["cpuval"]["title"],data["cpuval"]["xaxis"], data["cpuval"]["yaxis"], data["cpuval"]["legend"]);
    } else if ( _chart_type === "memory" ) {
        $("#pic_3").removeAttr("hidden");
        memChartsFunc("pic_3",data);
    } else if ( _chart_type === "disk") {
        $("#pic_4").removeAttr("hidden");
        diskChartsFunc("pic_4",data);
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
        title: { text:pic_title },
        tooltip: { trigger: 'axis' },                      // 轴对齐时展示所有点信息
        legend: {
            data: pic_legendArr,                           // y轴线的标签信息 **需要填充数据
            textStyle: { fontSize: 16 },
            icon:'roundRect'
        },
        grid: { containLabel:true },
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
            feature: { saveAsImage:{}, restore:{} }
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
    cpuChart.clear();
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
        title: { text: data["title"] },
        legend: { data:["used","free","buffers","cached"], icon:'roundRect' , left:'30%', },
        tooltip: {
            trigger: 'axis', formatter: function (params) {
                var ToolRes = [];
                for (var Par = 0; Par < params.length; Par++) {
                    if ( Par ===0 ) { ToolRes += params[Par].data[Par] + "<br\>"; }
                    var Val = params[Par].data[Par+1];
                    if ( Val > Math.pow(1024,3)) {
                        Val = ( Val/(Math.pow(1024,3)) ).toFixed(2)+"GB";
                    } else if ( Val > Math.pow(1024,2)) {
                        Val = ( Val/(Math.pow(1024,2)) ).toFixed(2)+"MB";
                    } else if ( Val > 1024 ) {
                        Val = ( Val/1024 ).toFixed(2)+"KB";
                    }
                    ToolRes += "<div style='display:inline-flex;border-radius:50%;"
                        + "width:10px;height:10px;background-color:"
                        + params[Par].color + "'></div> "
                        + params[Par].seriesName + " : " + Val + "<br\>";
                } return ToolRes;
            }
        },
        dataset: [{
            dimension: data["memval"]["legend"],
            source: dataSetmem
        }, {
            dimension: data["Memval"]["legend"],
            source: dataSetMem
        }],
        xAxis: { type: 'category', boundaryGap: false },
        yAxis: { gridIndex: 0,
            axisLabel:{
                formatter: function(value) {
                    var result = [];
                    if ( value > Math.pow(1024,3) ) {
                        result = ( value/(Math.pow(1024,3)) ).toFixed(2)+"GB";
                    } else if ( value >Math.pow(1024,2) ) {
                        result = ( value/(Math.pow(1024,2)) ).toFixed(2)+"MB";
                    } else if ( value > 1024 ) {
                        result = ( value/ 1024 ).toFixed(2)+"KB";
                    } else {
                        result = value;
                    } return result
                }
            }
        },
        grid: { top: '15%', left:'8%', right:'40%',containLabel:true },
        dataZoom: [{
            id: 'dataZoomX',
            type: 'slider',
            xAxisIndex:[0],
            filterMode:'filter',
        }, {
            handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-' +
            '1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z ' +
            'M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
            handleSize: '80%',
            handleStyle: { color: '#fff', shadowBlur: 3, shadowColor: 'rgba(0, 0, 0, 0.6)', shadowOffsetX: 2, shadowOffsetY: 2 },
        }],
        toolbox: {
            orient: 'horizontal',
            x: '90%',
            feature: { saveAsImage:{}, restore:{} }
        },
        color:["#de4d2c","#343a40","#848485","#322143"],
        series: [
            {type: 'line', name:'used', smooth:true, itemStyle: { normal: {lineStyle: {width: 3}}}, symbolSize: 5},
            {type: 'line', name:'free', smooth:true, itemStyle: { normal: {lineStyle: {width: 3}}}, symbolSize: 5},
            {type: 'line', name:'buffers', smooth:true, itemStyle: { normal: {lineStyle: {width: 3}}}, symbolSize: 5},
            {type: 'line', name:'cached', smooth:true, itemStyle: { normal: {lineStyle: {width: 3}}}, symbolSize: 5},
            {
                datasetIndex:0,
                label:{ formatter:'({d}%)',color:'#00aee7' },
                id:'pie', type: 'pie',
                radius: [ 0,'30%'],
                center: ['78%', '55%'],
                encode: { value: 0,tooltip: 0 },
                seriesLayoutBy: 'row',
            },{
                datasetIndex:1,
                label:{ formatter:'[{d}%]',color:'#e6bb2d' },
                id:'circle', type: 'pie',
                radius: ['40%', '50%'],
                center: ['78%', '55%'],
                encode: { value: 0,tooltip: 0 },
                seriesLayoutBy: 'row',
            }
        ]
    };
    var memChart = echarts.init(document.getElementById(div_id));
    memChart.on('updateAxisPointer', function (event) {
        var xAxisInfo = event.axesInfo[0];
        if (xAxisInfo) {
            var dimension = xAxisInfo.value;
            memChart.setOption({
                series: [{
                    datasetIndex:0, id:'pie',
                    // label: { formatter:'{@' + dimension + '} ({d}%)'},
                    label: { formatter:'({d}%)'},
                    encode: { value: dimension, tooltip: dimension },
                },{
                    datasetIndex:1, id:'circle',
                    encode: { value: dimension, tooltip: dimension },
                }]
            });
        }
    });
    memChart.clear();
    memChart.setOption(memOpts,true);
    window.addEventListener("resize",function() {
        memChart.resize();
    });
}

function diskChartsFunc(div_id,data) {
    var diskChartOpts = {
        title: { text: data["title"] },
        //legend: { data:data["diskval"]["legend"], icon:'roundRect' },
        legend: { data:["used"], icon:'roundRect' },
        tooltip: { trigger:'axis' },
        toolbox: {
            orient: 'horizontal',
            x: '90%',
            feature: { saveAsImage:{}, restore:{} }
        },
        dataZoom: [{
            id: 'dataZoomX',
            type: 'slider',
            xAxisIndex:[0],
            filterMode:'filter',
        }, {
            handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-' +
            '1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z ' +
            'M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
            handleSize: '80%',
            handleStyle: { color: '#fff', shadowBlur: 3, shadowColor: 'rgba(0, 0, 0, 0.6)', shadowOffsetX: 2, shadowOffsetY: 2 },
        }],
        xAxis: {
            type:'category',
            data: [1,2,3,4,5,6,7,8],
            //data: data["diskval"]["xasix"],
            axisLabel:{ textStyle:{ fontSize:14 } }
        },
        yAxis: {
            type:'value',
            axisLabel:{ textStyle:{ fontSize: 14 } }
        },
        color:'#33383d',
        series:[{
            data:[400,400,400,400,400,400,400,400],
            type:'bar',
            color:'#053401',
            barGap:'-100%'
        },{
            data:[100,180,300,200,340,60,52,120],
            type:'bar',
            color:'#69a78a',
            barGap:'-100%'
        }]
    };
    var diskChart = echarts.init(document.getElementById(div_id));
    diskChart.clear();
    diskChart.setOption(diskChartOpts,true);
    window.addEventListener("resize",function() {
        diskChart.resize();
    });
}