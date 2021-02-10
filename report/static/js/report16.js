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
        source01()
    })
});


var source01 = function () {
    var Title = '主要省份来货对比(单位: 吨)';
    var source01Title = '蔬菜来源地占比';
    var dayArr = []
    var lastDayArr = []
    var currentSourceArr = []
    var currentSourceArrTemp = []
    var currentDayData = []
    var currentDayDataTemp = []
    var lastSourceArr = []
    var lastSourceArrTemp = []
    var lastDayData = []
    var lastDayDataTemp = []
    var sourceTemp = []
    var dataToPie = []
    $(function () {
        $.ajax({
            type: "get",
            url: "/source",
            timeout: 100000,
            data: {year:nowYear, month:nowMonth, day:nowDay},
            success: function (data) {
                console.log(data)
                for (let i = 0; i < data[0].length; i++) {
                    currentSourceArrTemp.push(data[0][i][0])
                }

                for (let i = 0; i < data[1].length; i++) {
                    lastSourceArrTemp.push(data[1][i][0])
                }

                // 计算昨天今天来源地的交集
                currentSourceArrTemp.filter( item => {
                  if (lastSourceArrTemp.indexOf(item) > -1) {
                    sourceTemp.push(item)
                  }
                })

                // 去掉不在交集中的数据
                data[0].filter( item => {
                  if (sourceTemp.indexOf(item[0]) > -1) {
                    currentDayDataTemp.push(item)
                  }
                })

                data[1].filter( item => {
                  if (sourceTemp.indexOf(item[0]) > -1) {
                    lastDayDataTemp.push(item)
                  }
                })

                // console.log('排序之前', currentDayData, lastDayData)

                // 根据来源地进行排序
                currentDayDataTemp.sort((a, b) => {
                  return a[0].localeCompare(b[0])
                })

                lastDayDataTemp.sort((a, b) => {
                  return a[0].localeCompare(b[0])
                })

                // console.log('排序之后', currentDayData, lastDayData)
                for (let i = 0; i < currentDayDataTemp.length; i++) {
                  currentSourceArr.push(currentDayDataTemp[i][0])
                  currentDayData.push(currentDayDataTemp[i][1])
                  lastDayData.push(lastDayDataTemp[i][1])
                  dataToPie.push({"name": currentDayDataTemp[i][0], "value": currentDayDataTemp[i][1]})
                }

                // 格式化返回回来的时间data[2][0]
                data[2][0].split('-').forEach( item => {
                  lastDayArr.push(parseInt(item))
                })
                console.log(lastDayArr)
                dayArr.push(lastDayArr[0] + '月' + lastDayArr[1] + '日')
                dayArr.push(nowMonth + '月' + nowDay + '日')
                console.log(dayArr)

                source02(source01Title, dataToPie)


                var myChart = echarts.init(document.getElementById('source02'));
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
                            x : 'right',
                            data : dayArr
                        },
                        xAxis: {
                            name: '地区',
                            data: currentSourceArr
                        },
                        yAxis: {name: '吨'},
                        series: [
                            {
                                type: 'bar',
                                name: dayArr[0],
                                barWidth: 12,
                                data: lastDayData,
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
                                name: dayArr[1],
                                barWidth: 12,
                                data: currentDayData,
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
        })
    })
}
source01()

var source02 = function (source01Title, source02Data) {
  // 绘制图表id=cheliang。
  echarts.init(document.getElementById('source01')).setOption({
  title: {
      text: source01Title,
      x: 'center'
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
  series: {
      type: 'pie',
      radius: '50%',
      seriesName: '123',
      data: source02Data,
      label: {
          normal: {
              formatter: '{b}:{c}:({d}%)'
          }
      }
  }
});
};
