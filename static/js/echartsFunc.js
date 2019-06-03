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