var nowMonth, nowYear;
var date = new Date();
nowMonth = date.getMonth();
nowYear = date.getFullYear();
nowDay = date.getDate() - 1;


// {# 日历时间选择器 #}
$(function(){
    date = new Date();
    month = date.getMonth();
    year = date.getFullYear();
    day = date.getDate() - 1;
    dateStr = year + '-' + month + '-' + day;
    $('.date_picker').val(dateStr);
    $('.date_picker').date_input();
    $('.show').click(function () {
        var value = $('.date_picker').val();
        var dateArr = value.split('-');
        nowYear = dateArr[0];
        nowMonth = dateArr[1];
        nowDay = dateArr[2];
        console.log('value---------', value)
        contrast()
    })
});


var contrast = function () {
    var Title = '蔬菜每日来货量(单位: 吨)';
    var dateArr = []
    var currentYearData = []
    var lastYearData = []
    $(function () {
        $.ajax({
            type: "get",
            url: "/contrast",
            timeout: 100000,
            data: {year:nowYear, month:nowMonth, day:nowDay},
            success: function (data) {
                console.log(data)
                for (let i = 0; i < data[1].length; i++) {
                    dateArr.push(data[1][i][0].slice(5, 10))
                    currentYearData.push(data[1][i][1])
                    lastYearData.push(data[0][i][1])
                }
                console.log(dateArr, currentYearData, lastYearData)
                var myChart = echarts.init(document.getElementById('contrast'));
                var option = {
                        title: {
                            text: Title,
                            left:'center'
                        },
                        toolbox: {
                        　　show: true,
                        　　feature: {
                        　　　　saveAsImage: {
                        　　　　show:true,
                        　　　　excludeComponents :['toolbox'],
                        　　　　pixelRatio: 2
                        　　　　}
                        　　}
                        },
                        tooltip: {},
                         //菜单
                        legend : {
                            //菜单字体样式
                            // textStyle : {
                            //     color : 'white'
                            // },
                            //菜单位置
                            x : 'right',
                            //菜单数据
                            data : ['2019年', '2020年']
                        },
                        xAxis: {
                            name: '日期',
                            data: dateArr
                        },
                        yAxis: {name: '吨'},
                        series: [
                            {
                                type: 'bar',
                                name: '2019年',
                                barWidth: 15,
                                data: lastYearData,
                                itemStyle: {
                                    normal: {
                                        label: {
                                        show: true,
                                        position: 'top'
                                        }
                                    }
                                }
                            },
                            {
                                type: 'bar',
                                name: '2020年',
                                barWidth: 15,
                                data: currentYearData,
                                itemStyle: {
                                    normal: {
                                        label: {
                                        show: true,
                                        position: 'top'
                                        }
                                    }
                                }
                            }
                        ]
                    };
            
                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);

                // 生成折线图
                trend(dateArr, currentYearData, lastYearData)
            }
        })
    })
}
contrast()

var trend = function (dateArr, currentYearData, lastYearData) {
    var Title = '蔬菜每日来货趋势';
    var myChart = echarts.init(document.getElementById('trend'));
                var option = {
                        title: {
                            text: Title,
                            left:'center'
                        },
                        toolbox: {
                        　　show: true,
                        　　feature: {
                        　　　　saveAsImage: {
                        　　　　show:true,
                        　　　　excludeComponents :['toolbox'],
                        　　　　pixelRatio: 2
                        　　　　}
                        　　}
                        },
                        tooltip: {},
                         //菜单
                        legend : {
                            //菜单字体样式
                            // textStyle : {
                            //     color : 'white'
                            // },
                            //菜单位置
                            x : 'right',
                            //菜单数据
                            data : ['2019年', '2020年']
                        },
                        xAxis: {
                            name: '日期',
                            data: dateArr
                        },
                        yAxis: {name: '吨'},
                        series: [
                            {
                                type: 'line',
                                name: '2019年',
                                barWidth: 15,
                                data: lastYearData,
                                itemStyle: {
                                    normal: {
                                        label: {
                                        show: true,
                                        position: 'top'
                                        }
                                    }
                                }
                            },
                            {
                                type: 'line',
                                name: '2020年',
                                barWidth: 15,
                                data: currentYearData,
                                itemStyle: {
                                    normal: {
                                        label: {
                                        show: true,
                                        position: 'top'
                                        }
                                    }
                                }
                            }
                        ]
                    };
            
                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
}