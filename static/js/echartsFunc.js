function CreateChartFunc(_chart_ip, _chart_type,data) {
    $("#chart_title").html("<i class='fa fa-yelp'></i><strong>&nbsp;" + _chart_type.toUpperCase() +
        "</strong>&nbsp;Charts For &nbsp;<strong>" + _chart_ip + "</strong>" );
    var typeArr = ["cpu","disk","memory","network"];
    for (var Pic=0; Pic< typeArr.length; Pic++) {
        $("#pic_"+typeArr[Pic]).attr("hidden","hidden");
    }
    if ( _chart_type === "cpu" ) {
        $("#pic_cpu").removeAttr("hidden");
        cpuEchartsFunc("pic_cpu", data["loadval"]["title"],data["loadval"]["xaxis"], data["loadval"]["yaxis"], data["loadval"]["legend"],data);
        // cpuEchartsFunc("pic_2", data["cpuval"]["title"],data["cpuval"]["xaxis"], data["cpuval"]["yaxis"], data["cpuval"]["legend"]);
    } else if ( _chart_type === "disk") {
        $("#pic_disk").removeAttr("hidden");
        diskChartsFunc("pic_disk",data);
        $("#disk_swiper").ready( function () {
            var swiper = new Swiper('.swiper-container', {
                noSwiping: true,
                noSwipingClass: 'stop-swiping',
                nextButton: '.swiper-button-next',
                prevButton: '.swiper-button-prev',
            });
        })
    } else if ( _chart_type === "memory" ) {
        $("#pic_memory").removeAttr("hidden");
        memChartsFunc("pic_memory",data);
    }
}

function cpuEchartsFunc(div_id,pic_title,pic_xaxis,pic_yaxis,pic_legendArr,data){
    var seriesArr = [];
    console.log(data);
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
        title: { text:pic_title, left:'10%' },
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
            x: '85%',
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
        title: { text: data["title"], left:'10%' },
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
            name: 'mem',
            dimension: data["memval"]["legend"],
            source: dataSetmem
        }, {
            name: 'Mem',
            dimension: data["Memval"]["legend"],
            source: dataSetMem
        }],
        xAxis: { type: 'category', boundaryGap: false },
        yAxis: { name:'memory',
            gridIndex: 0,
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
            x: '85%',
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
                label: {
                    formatter:function(event) {
                        var _dataName = event.seriesName.split(",");
                        return "(" + _dataName[event.dataIndex+1] + ":" + [event.percent]+ "%" + ")";
                    }, color: '#00AEE7'
                },
                name: data["memval"]["legend"],
                id:'pie', type: 'pie',
                radius: [ 0,'30%'],
                center: ['78%', '55%'],
                encode: { value: 0,tooltip: 0 },
                seriesLayoutBy: 'row',
            },{
                datasetIndex:1,
                label:{
                    formatter:function(event) {
                        var _dataName = event.seriesName.split(",");
                        return "[" + _dataName[event.dataIndex+1] + ":" + [event.percent]+ "%" + "]";
                    }, color:'#e6bb2d'
                },
                name: data["Memval"]["legend"],
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
                    label: {
                        formatter:function(event) {
                            var _dataName = event.seriesName.split(",");
                            return "(" + _dataName[event.dataIndex+1] + ":" + [event.percent]+ "%" + ")";
                        }
                    },
                    encode: { value: dimension, tooltip: dimension },
                },{
                    datasetIndex:1, id:'circle',
                    label: {
                        formatter:function(event) {
                            var _dataName = event.seriesName.split(",");
                            return "[" + _dataName[event.dataIndex+1] + ":" + [event.percent]+ "%" + "]";
                        }
                    },
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
    var mountArr = data["diskval"]["mount"].split("[")[1].split("]")[0].split(", ");
    var sourceArr = [];
    var seriesArr = [];
    var MultdiskChart = [];
    for (var m = 0; m < mountArr.length; m++) {
        seriesArr.push({
            datasetIndex: m,
            type: 'bar',
            name: mountArr[m] + ' Total',
            color: '#e9ecef',
            barGap: '-100%',
            yAxisIndex: 1,
            encode: {x: "checktime", y: "total"},
        }, {
            datasetIndex: m,
            type: 'bar',
            name: mountArr[m] + ' Used',
            color: '#343A40',
            barGap: '-100%',
            yAxisIndex: 1,
            encode: {x: "checktime", y: "used"},
        }, {
            datasetIndex: m,
            type: 'line',
            name: mountArr[m] + ' Inode',
            encode: {x: "checktime", y: "inode"},
            yAxisIndex: 0,
            itemStyle: {normal: {lineStyle: {width: 3}}},
            symbolSize: 5
        });
        var _valArr = [];
        _valArr.push(["checktime", "total", "used", "inode", "percent"]);
        for (var v in data["diskval"]["value"][m]) {
            if (data["diskval"]["value"][m].hasOwnProperty(v)) {
                var Obj = JSON.parse(data["diskval"]["value"][m][v]);
                $.each(Obj, function (key, val) {
                    var _val = [];
                    _val.push(data["diskval"]["axis"][v], Obj["total"], Obj["used"], parseInt(Obj["inode"]), parseInt(Obj["percent"]));
                    _valArr.push(_val);
                    return false;
                });
            }
        }
        sourceArr.push({source: _valArr});
        var diskChartOpts = {
            title: {text: data["title"], left: '10%'},
            legend: {data: data["diskval"]["legend"], icon: 'roundRect'},
            tooltip: {
                trigger: 'axis', axisPointer: {type: 'cross'},
                formatter: function (params) {
                    var ToolRes = [];
                    for (var Par = 0; Par < params.length; Par++) {
                        if (Par === 0) {
                            ToolRes += params[Par].data[Par] + "<br\>";
                        }
                        var Val = params[Par].data[Par + 1];
                        if (Val > Math.pow(1024, 4)) {
                            Val = (Val / (Math.pow(1024, 4))).toFixed(2) + "TB";
                        } else if (Val > Math.pow(1024, 3)) {
                            Val = (Val / (Math.pow(1024, 3))).toFixed(2) + "GB";
                        } else if (Val > Math.pow(1024, 2)) {
                            Val = (Val / (Math.pow(1024, 2))).toFixed(2) + "MB";
                        } else if (Val > 1024) {
                            Val = (Val / 1024).toFixed(2) + "KB";
                        }
                        if (params[Par].componentSubType === "line") {
                            ToolRes += "<div style='display:inline-flex;border-radius:50%;width:10px;height:10px;background-color:"
                                + params[Par].color + "'></div> " + params[Par].seriesName + " : " + Val + "<span>%</span><br\>";
                        } else {
                            ToolRes += "<div style='display:inline-flex;border-radius:50%;width:10px;height:10px;background-color:"
                                + params[Par].color + " '></div> " + params[Par].seriesName + " : " + Val + "<br\>";
                        }
                    }
                    return ToolRes;
                }
            },
            toolbox: {
                orient: 'horizontal',
                x: '85%',
                feature: {saveAsImage: {}, restore: {}}
            },
            dataset: sourceArr,
            dataZoom: [{
                id: 'dataZoomX',
                type: 'slider',
                xAxisIndex: [0],
                filterMode: 'filter',
            }, {
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
                },
            }],
            xAxis: {
                type: 'category',
                axisLabel: {textStyle: {fontSize: 14}}
            },
            yAxis: [{
                name: 'Inode',
                type: 'value',
                position: 'right',
                max: 100,
                axisLabel: {textStyle: {fontSize: 14}}
            }, {
                name: 'Disk',
                type: 'value',
                position: 'left',
                axisLabel: {
                    textStyle: {fontSize: 14},
                    formatter: function (value) {
                        var result = [];
                        if (value > Math.pow(1024, 4)) {
                            result = (value / (Math.pow(1024, 4))).toFixed(2) + "TB";
                        } else if (value > Math.pow(1024, 3)) {
                            result = (value / (Math.pow(1024, 3))).toFixed(2) + "GB";
                        } else if (value > Math.pow(1024, 2)) {
                            result = (value / (Math.pow(1024, 2))).toFixed(2) + "MB";
                        } else if (value > 1024) {
                            result = (value / 1024).toFixed(2) + "KB";
                        } else {
                            result = value;
                        }
                        return result
                    }
                }
            }],
            series: seriesArr
        };
        if ( mountArr.length === 1 ) {
            $("#" + div_id).removeAttr("_echarts_instance_").empty();
            var diskChart = echarts.init(document.getElementById(div_id));
            diskChart.clear();
            diskChart.setOption(diskChartOpts, true);
            window.addEventListener("resize", function () {
                diskChart.resize();
            });
        } else {
            seriesArr = [];
            var MultdiskWeb = "";
            var MultDiskDiv = "<div id='" + div_id + "_" + m + "' style='width:94vw;height:60vh;margin-bottom:2%' " +
                "class='swiper-slide stop-swiping'></div>";
            if ( m === 0 ) {
                MultdiskWeb += "<div id='disk_swiper' class='swiper-container'><div class='swiper-wrapper'>";
                MultdiskWeb += MultDiskDiv;
                $("#" + div_id).html(MultdiskWeb);
            } else if ( m === mountArr.length-1  ) {
                MultdiskWeb += MultDiskDiv;
                MultdiskWeb += "</div></div>";
                $(".swiper-wrapper").append(MultdiskWeb);
                $(".swiper-container").append("<div class='swiper-button-prev'></div>" +
                    "<div class='swiper-button-next'></div>");
            } else {
                MultdiskWeb += MultDiskDiv;
                $(".swiper-wrapper").append(MultdiskWeb);
            }
            MultdiskChart[m] = echarts.init( document.getElementById(div_id+"_"+m) );
            MultdiskChart[m].clear();
            MultdiskChart[m].setOption(diskChartOpts,true);
            if ( m === mountArr.length -1 ) {
                $.each(MultdiskChart, function(key,val) {
                    window.addEventListener("resize", function () {
                        val.resize();
                    });
                });
            }
        }
    }
}