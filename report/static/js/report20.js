var nowMonth, nowYear;
var date = new Date();
nowMonth = date.getMonth() + 1;
nowYear = date.getFullYear();
nowDay = date.getDate() - 1;

// report15--来货总量对比
var contrast = function () {
    var Title = '蔬菜每日来货量(单位: 吨)';
    // 时间数据
    var dateArr = []
    var currentYearData = []
    var lastYearData = []
    // 库存数据
    var stockDateArr = []
    var stockData = []
    $(function () {
        $.ajax({
            type: "get",
            url: "/contrast",
            timeout: 100000,
            data: {year:nowYear, month:nowMonth, day:nowDay},
            success: function (data) {
                console.log('data------', data)
                for (let i = 0; i < data[1].length; i++) {
                    dateArr.push(data[1][i][0].slice(5, 10))
                    stockDateArr.push(data[1][i][0])
                    currentYearData.push(data[1][i][1])
                    lastYearData.push(data[0][i][1])
                    stockData.push(data[2][i][1])
                }
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
                        legend : {
                            x : 'right',
                            data : [(nowYear - 1) + '年', nowYear + '年']
                        },
                        xAxis: {
                            name: '日期',
                            data: dateArr
                        },
                        yAxis: {name: '吨'},
                        series: [
                            {
                                type: 'bar',
                                name: (nowYear - 1) + '年',
                                barWidth: 12,
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
                                name: nowYear + '年',
                                barWidth: 12,
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

                // 生成表5的蔬菜进销存统计的表格
                stockTable(stockDateArr, currentYearData, stockData)

                // contrast_analysis生成分析文字
                contrast_analysis(currentYearData, lastYearData, stockData)
            }
        })
    })
}
// contrast()


// contrast_analysis生成分析文字
var contrast_analysis = function (currentYearData, lastYearData, stockData) {
    var currentLen = currentYearData.length
    var lastLen = lastYearData.length
    var currentDayData = currentYearData[currentLen - 1]
    var lastDayData = currentYearData[currentLen - 2]
    var lastYearDayData = lastYearData[lastLen - 1]

    // 增加或者下降 
    var type1 = ''
    var type2 = ''
    // 与昨日比
    type1 = (currentDayData > lastDayData) ? '增加' : '下降'
    // 与去年比
    type2 = (currentDayData > lastYearDayData) ? '增加' : '下降'

    // 与昨日比
    var type1Ratio = ''
    // 与去年比
    var type2Ratio = ''

    type1Ratio = Math.abs(((currentDayData - lastDayData) / lastDayData * 100).toFixed(0)) + '%'
    type2Ratio = Math.abs(((currentDayData - lastYearDayData) / lastYearDayData * 100).toFixed(0)) + '%'
    var text = `1. ${nowYear}年${nowMonth}月${nowDay}日，深圳海吉星市场蔬菜来货总量合计${currentDayData}吨， 与昨日(${lastDayData}吨)相比${type1}${Math.abs(currentDayData - lastDayData)}吨，${type1.slice(0, 1)}幅为${type1Ratio}；与${nowYear - 1}年同期(${lastYearDayData}吨)相比${type2}${Math.abs(currentDayData - lastYearDayData)}吨，${type2.slice(0,1)}幅为${type2Ratio}。截止至${nowMonth}月${nowDay}日23点30分，市场蔬菜档位库存量约为${stockData[stockData.length - 1]}吨。`
  
    $(function () {
        $('.contrast_analysis').html(text)
    })

    $(function () {
        $('.summary_contrast_analysis').html(text)
    })
}




// report15--来货总量对比
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
            legend : {
                x : 'right',
                data : [(nowYear - 1) + '年', nowYear + '年']
            },
            xAxis: {
                name: '日期',
                data: dateArr
            },
            yAxis: {name: '吨'},
            series: [
                {
                    type: 'line',
                    name: (nowYear - 1) + '年',
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
                    name: nowYear + '年',
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

// 表5的蔬菜进销存统计的表格
var stockTable = function (stockDateArr, currentYearData, stockData) {
    var tableArr = []
    var sold = 0
    for (let i = 1; i < stockDateArr.length; i++) {
        sold = currentYearData[i] + stockData[i - 1] - stockData[i]
        tableArr.push([stockDateArr[i], currentYearData[i], sold, stockData[i]])
    }
    // 处理其它
    len = tableArr.length
    for (let i = len - 1; i >= 0; i--) {
        htmlStr = `<tr class="js-add"><td>${tableArr[i][0]}</td><td>${tableArr[i][1]}</td><td>${tableArr[i][2]}</td><td>${tableArr[i][3]}</td></tr>`
        $('.js-stock-head').after(htmlStr)
    }
    download_stock_table()

}


// 处理下载
var download_stock_table = function () {
    $(function () {
        // 使用outerHTML属性获取整个table元素的HTML代码（包括<table>标签），然后包装成一个完整的HTML文档，设置charset为urf-8以防止中文乱码
        var html = "<html><head><meta charset='utf-8' /></head><body>" + document.getElementsByTagName("table")[1].outerHTML + "</body></html>";
        // 实例化一个Blob对象，其构造函数的第一个参数是包含文件内容的数组，第二个参数是包含文件类型属性的对象
        var blob = new Blob([html], { type: "application/vnd.ms-excel" });
        // var a = document.getElementsByTagName("a")[0];
        var a = document.getElementsByClassName("download_stock_table")[0];
        // 利用URL.createObjectURL()方法为a元素生成blob URL
        a.href = URL.createObjectURL(blob);
        // 设置文件名
        var title = "蔬菜进销存统计" + ".xls";
        a.download = title;
    });
  };



// report18--来货类型对比
var type_compare = function () {
  // 鲜菜类
  var type1Data = []
  // 硬口类
  var type2Data = []
  var currentTime = ''
  var lastTime = ''
  var typeArr = ["鲜菜类", "硬口类"]
  $(function () {
      $.ajax({
          type: "get",
          url: "/baobiao18_source",
          timeout: 100000,
          data: {year:nowYear, month:nowMonth, day:nowDay},
          success: function (data) {
              currentTime = data[1].shift()
              lastTime = data[0].shift()

              type1Data.push(data[0][0])
              type1Data.push(data[1][0])
              
              type2Data.push(data[0][1])
              type2Data.push(data[1][1])

              var myChart = echarts.init(document.getElementById('type_compare'));
              var option = {
                      title: {
                          text: "各品类来货量对比(单位: 吨)",
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
                          data : typeArr
                      },
                      xAxis: {
                          name: '日期',
                          data: [lastTime, currentTime]
                      },
                      yAxis: {name: '吨'},
                      series: [
                          {
                              type: 'bar',
                              name: typeArr[0],
                              barWidth: 35,
                              data: type1Data,
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
                              name: typeArr[1],
                              barWidth: 35,
                              data: type2Data,
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
              
              // type_compare生成分析文字
              type_compare_analysis(type1Data, type2Data)
          }
      })
  })
}
// type_compare()


// type_compare生成分析文字
var type_compare_analysis = function (type1Data, type2Data) {
    // 增加或者下降 
    var type1 = ''
    var type2 = ''
    var type1Ratio = ''
    var type2Ratio = ''
    type1 = (type1Data[1] > type1Data[0]) ? '上升' : '下降'
    type2 = (type2Data[1] > type2Data[0]) ? '上升' : '下降'
    type1Ratio = Math.abs(((type1Data[1] - type1Data[0]) / type1Data[0] * 100).toFixed(0)) + '%'
    type2Ratio = Math.abs(((type2Data[1] - type2Data[0]) / type2Data[0] * 100).toFixed(0)) + '%'
    var text = `2.蔬菜来货品类中，鲜菜类来货${type1Data[1]}吨， 环比${type1}${type1Ratio}； 硬口类来货${type2Data[1]}吨，环比${type2}${type2Ratio}。`
  
    $(function () {
        $('.type_compare_analysis').html(text)
    })

    $(function () {
        $('.summary_type_compare_analysis').html(text)
    })
}
// type_compare_analysis()

// report16----来源地分析
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
              // console.log(data)
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

              // console.log('排序之后', currentDayData, lastDayData)
              for (let i = 0; i < currentDayDataTemp.length; i++) {
                currentSourceArr.push(currentDayDataTemp[i][0])
                currentDayData.push(currentDayDataTemp[i][1])

                // 根据currentDayData的顺序收集lastDayData
                for (let j = 0; j < lastDayDataTemp.length; j++) {
                  if (currentDayDataTemp[i][0] == lastDayDataTemp[j][0]) {
                      lastDayData.push(lastDayDataTemp[j][1])
                      break
                  }
                }
                dataToPie.push({"name": currentDayDataTemp[i][0], "value": currentDayDataTemp[i][1]})
              }

              // 对饼图的数据进行排序
              dataToPie.sort((a, b) => {
                  return b["value"] - a["value"]
              })
              // 格式化返回回来的时间data[2][0]
              data[2][0].split('-').forEach( item => {
                lastDayArr.push(parseInt(item))
              })
              dayArr.push(lastDayArr[0] + '月' + lastDayArr[1] + '日')
              dayArr.push(nowMonth + '月' + nowDay + '日')
              // console.log('dataToPie', dataToPie)

            //   source02(source01Title, dataToPie)
              source03(source01Title, dataToPie)

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
                              barWidth: 15,
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
                              barWidth: 15,
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

              // 生成来源地文字分析
              source_analysis(currentSourceArr, currentDayData, lastDayData, data[0])
          }
      })
  })
}
// source01()



var source03 = function (source01Title, dataToPie) {

// console.log(source01Title, dataToPie)

    var myChart = echarts.init(document.getElementById('source03'))

let markLineData = []
// let source = [
//     ['product', '2015', '2016'],
//     ['系列1-1', 43.3],
//     ['系列1-2', 83.1],
//     ['系列1-3', 86.4],
//     ['系列1-4', 72.4],
//     ['系列1-5', 72.4],
//     ['系列2-1', 53.9],
//     ['系列2-2', 85.8],
//     ['系列2-3', 145.8],
// ]

let source = [
    ['province', '2015', '2016']
]
let otherLen = 0
let sum = 0
for (let i = 0; i < dataToPie.length; i++) {
    source.push([dataToPie[i].name, dataToPie[i].value])
    sum += dataToPie[i].value
    // 小于200吨的都归为其它
    if (otherLen === 0 && dataToPie[i].value < 150) {
        otherLen = dataToPie.length - i
    }
}

// 处理百分比的问题
var percent = ''
for (let i = 1; i < source.length; i++) {
    percent = ' ' + ((source[i][1] / sum) * 100).toFixed(1) + '%'
    source[i][0] += percent 
}

console.log(otherLen)

// 添加“其他”
addOtherData(source, otherLen);

option = {
    title: {
        text: source01Title,
        x: 'center'
    },
    // legend: {},
    // tooltip: {},
    dataset: {
        source: source
    },
    series: [{
            type: 'pie',
            radius: "50%",
            center: ['25%', '50%'],
            label: {
                show: true,
                position: "inside",
            },
            startAngle: 45, // 起始角度 45 
            clockwise: false, // 逆时针 
            markLine: {
                lineStyle: {
                    type: 'solid',
                    color: "#BFBFBF"
                },
                symbol: 'none',
                data: markLineData
            }
        },
        {
            type: 'pie',
            radius: "30%",
            center: ['75%', '50%'],
            encode: {
                itemName: 'province',
                value: '2016',
            },
            label: {
                show: true,
                position: ""
            },
        }
    ]
};
console.log('option-----', option)
 myChart.setOption(option);

// 获取表标线 对应点坐标
function getMarkLineData(percent) {
    // 1.获取画布 width,height
    let height = myChart.getHeight()
    let width = myChart.getWidth()

    // 2.  根据 series[0].center 获取圆心坐标
    let x0 = width * 0.25 // 圆心x轴坐标

    //3.圆边上点坐标
    // let x1   =   x0   +   r   *   cos(ao   *   3.14   /180   )
    // let y1   =   y0   +   r   *   sin(ao   *   3.14   /180   )

    // “其他” 终点坐标series[0].startAngle 45
    let x1 = x0 + (height / 4) * Math.cos(45 * 3.14 / 180)
    let y1 = (height * 0.5) - (height / 4) * Math.sin(45 * 3.14 / 180)

    let ao = 360 * (percent / 100) // 扇形角度

    let ao1 = 0 // 用来计算的坐标角度
    ao1 = (ao <= 45) ? (45 - ao) : (360 - (ao - 45))
    if (ao1 < 270 && ao1 > 45) ao1 = 270 // 角度当270用，要不样式不好看

    let x2 = 0,
        y2 = 0;
    x2 = x0 + (height / 4) * Math.cos(ao1 * 3.14 / 180)
    y2 = (height * 0.5) - (height / 4) * Math.sin(ao1 * 3.14 / 180)

    return [
        [{
            x: x1,
            y: y1
        }, {
            x: "75%",
            y: "35%"
        }],
        [{
            x: x2,
            y: y2
        }, {
            x: "75%",
            y: "65%"
        }]
    ]
}
// 添加其他 
function addOtherData(datasetSource, len) {
    let percent = 0
    let sum = 0 // 总计
    datasetSource.forEach((data, rowIndex) => {
        if (rowIndex > 0) {
            let count = 0
            for (let key of data) {
                let value = isNaN(key) ? 0 : Number(key)
                if (count === 1) sum += value
                count++
            }
        }
    })
    let endData = datasetSource.slice(datasetSource.length - len)
    let other = ["其他"]
    for (let i = 0; i < endData.length; i++) {
        let j = 0;
        for (let key of endData[i]) {
            let value = isNaN(key) ? 0 : key
            if (j) other[j] ? (other[j] += value) : other.push(value)
            j++
        }
        endData[i].splice(1, 0, "")
    }
    datasetSource.push(other)
    // 处理其他的占比
    let sumAll = 0
    let sumLen = 0
    for (let i = 1; i < datasetSource.length - 1; i++) {
        sumAll += datasetSource[i][datasetSource[i].length - 1]
        if (i >= len) {
            sumLen += datasetSource[i][datasetSource[i].length - 1]
        }
    }

    console.log(sumAll, sumLen)
    datasetSource[datasetSource.length - 1][0] += ' ' + ((sumLen / sumAll) * 100).toFixed(1) + '%'
    console.log(sum)


    console.log('datasetSource-----', datasetSource)
    // "其他"占比
    percent = sum ? ((other[1] / sum) * 100).toFixed(2) : 100
    markLineData = getMarkLineData(percent)
    console.log('markLineData-----', markLineData)
}
}



















var source_analysis = function (currentSourceArr, currentDayData, lastDayData, currentSource) {
    // console.log('analysis', currentDayData, lastDayData)
    var sum = 0
    var len = currentDayData.length
    var currentSourceLen = currentSource.length
    var ratio1 = ''
    var ratio2 = ''
    var ratio3 = ''
    // 变动的数值
    var changeNum = 0
    var changeArr01 = []
    var changeArr02 = []
    // 变动前3的数据数组
    var changeArr = []
    for (let i = 0; i < len; i++) {
        changeNum = currentDayData[i] - lastDayData[i]
        changeArr01.push(changeNum)
        changeArr02.push(changeNum)
        sum += currentDayData[i]
    }

    ratio1 = (currentDayData[0] / sum * 100).toFixed(0) + '%'
    ratio2 = (currentDayData[1] / sum * 100).toFixed(0) + '%'
    ratio3 = (currentDayData[2] / sum * 100).toFixed(0) + '%'
    // console.log(changeArr01)

    

    // 找出变动幅度在前3的数据
    changeArr01.sort((a, b) => {
        return Math.abs(b) - Math.abs(a)
    })
    // console.log('after', changeArr01)

    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < len; j++) {
            if (changeArr01[i] === changeArr02[j]) {
                var type = changeArr01[i] > 0 ? '增加' : '减少'
                var num = Math.abs(changeArr01[i])
                var ratio = Math.abs((changeArr01[i] / lastDayData[j] * 100).toFixed(0)) + '%'
                var location = currentSourceArr[j]
                changeArr.push([location, type + num + '吨', type.slice(0, 1) + '幅' + ratio]) 
            }
        }
    }

    var text = `1.来货产地结构方面， 共计有${currentSourceLen}个产地来货，其中主要以${currentSourceArr[0]}、${currentSourceArr[1]}及${currentSourceArr[2]}为主，分别占比${ratio1}、${ratio2}、${ratio3}。
                <br/>2.与昨日相比来货变动较大的产地主要有${changeArr[0][0]}(${changeArr[0][1]}，${changeArr[0][2]})、${changeArr[1][0]}(${changeArr[1][1]}，${changeArr[1][2]})、${changeArr[2][0]}(${changeArr[2][1]}，${changeArr[2][2]})。`

    var text02 = `3.来货产地结构方面， 共计有${currentSourceLen}个产地来货，其中主要以${currentSourceArr[0]}、${currentSourceArr[1]}及${currentSourceArr[2]}为主，分别占比${ratio1}、${ratio2}、${ratio3}。
                <br/>4.与昨日相比来货变动较大的产地主要有${changeArr[0][0]}(${changeArr[0][1]}，${changeArr[0][2]})、${changeArr[1][0]}(${changeArr[1][1]}，${changeArr[1][2]})、${changeArr[2][0]}(${changeArr[2][1]}，${changeArr[2][2]})。`
    
    $(function () {
        $('.source_analysis').html(text)
    })

    $(function () {
        $('.summary_source_analysis').html(text02)
    })
}




// report16----来源地分析
var source02 = function (source01Title, source02Data) {
  // console.log('source02', source02Data)
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
            formatter: '{b} {d}%'
        }
    }
}
});
};



// report17--均价趋势
var price_trend = function () {
  var Title = '重点监测20个蔬菜单品均价(单位: 元/kg)'
  var resArr = []
  var xArr = []
  var yArr = []
  $(function () {
      $.ajax({
          type: "get",
          url: "average_price",
          timeout: 100000,
          data: {year:nowYear, month:nowMonth, day:nowDay},
          success: function (res) {
              // 取出均价趋势的数据
              var data = res[0]

              // 取出2天环比的数据
              var data02 = res[1]
              console.log('data02', data02)

              // 取出时间
              var currentTime = res[2]
              var lastTime = res[3]

              // 处理返回的单品均价数据
              for (let i = 0; i < data.length; i++) {
                  var time = new Date(data[i][0])
                  var data_month = time.getMonth() + 1
                  var data_day = time.getDate()

                  if (data_day == nowDay && data_month == nowMonth) {
                      resArr = data.slice(i - 22, i + 1)
                      break
                  }
              }

              for (let i = 0; i < resArr.length; i++) {
                  xArr.push(resArr[i][0].slice(5))
                  yArr.push(resArr[i][1])
              }

              var myChart = echarts.init(document.getElementById('price_trend'));
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
                  xAxis: {
                      name: '日期',
                      data: xArr
                  },
                  yAxis: {name: '元/kg'},
                  series: [
                      {
                          type: 'line',
                          name: nowYear + '年',
                          barWidth: 15,
                          data: yArr,
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


              // 处理2天环比的数据并生成表格
              handle_price_table(data02, currentTime, lastTime)

              // 价格统计的文字分析
              price_trend_analysis(data02, data)
          }
      })
  })
}
// price_trend()


// 价格统计的文字分析
var price_trend_analysis = function (data02, data) {
    console.log(data)
    // 计算价格波动最大的值
    var max = Math.abs(data02[0][4].split('%')[0])
    var temp = 0
    for (let i = 1; i < data02.length - 1; i++) {
        temp = Math.abs(data02[i][4].split('%')[0])
        if (max < temp) {
            max = temp
        }
    }

    max = Math.ceil(max) + '%'
    var type = ''
    if ( Number(data[data.length - 1]) > Number(data[data.length - 2])) {
        type = '有所增加'
    } else if (Number(data[data.length - 1]) === Number(data[data.length - 2])) {
        type = '持平'
    } else {
        type = '有所减少'
    }
    
    var text = `1.重点监测的20个蔬菜单品整体均价为${data[data.length - 1][1]}元/kg, 与昨日持平，波动较大的产品为大白菜(上升47.1%)、西红柿(上升28.6%)、莴笋(上升23.3%)、胡萝卜(上升16.7%)、茄子(下降13.3%)、豆角(上升10%)。
    其它所有产品价格波动均在10%以内。`

    var text02 = `6.重点监测的20个蔬菜单品整体均价为${data[data.length - 1][1]}元/kg, 与昨日持平，波动较大的产品为大白菜(上升47.1%)、西红柿(上升28.6%)、莴笋(上升23.3%)、胡萝卜(上升16.7%)、茄子(下降13.3%)、豆角(上升10%)。
                其它所有产品价格波动均在10%以内。`
        
    $(function () {
        $('.price_trend_analysis').html(text)
        $('.summary_price_trend_analysis').html(text02)
    })
}



// 处理2天环比的数据并生成表格
var handle_price_table = function (data02, currentTime, lastTime) {
  $('.js-time1').text(lastTime)
  $('.js-time2').text(currentTime)
  var len = data02.length
  // 处理均价
  if (len > 1) {
      // 处理均价
      htmlStr = `<tr class="js-add"><td colspan="2">均价</td><td>${data02[len - 1][0]}</td><td>${data02[len - 1][1]}</td><td>${data02[len - 1][2]}</td></tr>`
      $('.js-price-head').after(htmlStr) 

      // 处理其它
      for (let i = 0; i < data02.length - 1; i++) {
          htmlStr = `<tr class="js-add"><td>${data02[i][0]}</td><td>${data02[i][1]}</td><td>${data02[i][2]}</td><td>${data02[i][3]}</td><td>${data02[i][4]}</td></tr>`
          $('.js-price-head').after(htmlStr)
      }
      download_price_table()
  }
}

// 处理下载
var download_price_table = function () {
  $(function () {
      // 使用outerHTML属性获取整个table元素的HTML代码（包括<table>标签），然后包装成一个完整的HTML文档，设置charset为urf-8以防止中文乱码
      var html = "<html><head><meta charset='utf-8' /></head><body>" + document.getElementsByTagName("table")[0].outerHTML + "</body></html>";
      // 实例化一个Blob对象，其构造函数的第一个参数是包含文件内容的数组，第二个参数是包含文件类型属性的对象
      var blob = new Blob([html], { type: "application/vnd.ms-excel" });
      // var a = document.getElementsByTagName("a")[0];
      var a = document.getElementsByClassName("download_price_table")[0];
      // 利用URL.createObjectURL()方法为a元素生成blob URL
      a.href = URL.createObjectURL(blob);
      // 设置文件名
      var title = "蔬菜价格统计" + ".xls";
      a.download = title;
  });
};


// report18---销售去向分析
var sales_destination = function () {
  source01Data = [
      {name: "商超", value: 29},
      {name: "供港", value: 21},
      {name: "二批市场", value: 20},
      {name: "农贸市场", value: 17},
      {name: "餐饮、饭堂", value: 13}
  ]
echarts.init(document.getElementById('sales_destination')).setOption({
title: {
    text: "蔬菜销售渠道占比",
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
    data: source01Data,
    label: {
        normal: {
            formatter: '{b} {d}%'
        }
    }
}
});
};
// sales_destination()

// 供应情况
var supply = function () {
  $(function () {
      $.ajax({
          type: "get",
          url: "baobiao19_supply",
          timeout: 100000,
          data: {year:nowYear, month:nowMonth, day:nowDay},
          success: function (data) {
              handle_supply_table(data)
          }
      })
  })
}
// supply()

// 生成表格
var handle_supply_table = function (data) {
  var len = data.length
  // 处理均价
  if (len > 1) {
      var sum = data.pop()
      // 处理合计
      htmlStr = `<tr class="js-add"><td colspan="3">合计</td><td>${sum[0]}</td><td>${sum[1]}</td></tr>`
      $('.js-supply-head').after(htmlStr)

      // 处理其它
      len = data.length
      for (let i = len - 1; i >= 0; i--) {
          htmlStr = `<tr class="js-add"><td>${i + 1}</td><td>${data[i][0]}</td><td>${data[i][1]}</td><td>${data[i][2]}</td><td>${data[i][3]}</td></tr>`
          $('.js-supply-head').after(htmlStr)
      }
      download_supply_table()

      supply_analysis(sum)
  }
}

var supply_analysis = function (data) {
    console.log('supply----', data)
    var text = `7.市场前20名客户总来货量为${data[0]}吨， 占总来货量的${data[1]}`
    $(function () {
        $('.summary_supply_analysis').html(text)
    })
}

// 处理下载
var download_supply_table = function () {
  $(function () {
      // 使用outerHTML属性获取整个table元素的HTML代码（包括<table>标签），然后包装成一个完整的HTML文档，设置charset为urf-8以防止中文乱码
      var html = "<html><head><meta charset='utf-8' /></head><body>" + document.getElementsByTagName("table")[2].outerHTML + "</body></html>";
      // 实例化一个Blob对象，其构造函数的第一个参数是包含文件内容的数组，第二个参数是包含文件类型属性的对象
      var blob = new Blob([html], { type: "application/vnd.ms-excel" });
      // var a = document.getElementsByTagName("a")[0];
      var a = document.getElementsByClassName("download_supply_table")[0];
      // 利用URL.createObjectURL()方法为a元素生成blob URL
      a.href = URL.createObjectURL(blob);
      // 设置文件名
      var title = "蔬菜前20名客户供应情况" + ".xls";
      a.download = title;
  });
};


// 市场动态及问题
var dynamic_problem = function () {
    $(function () {
        $.ajax({
            type: "get",
            url: "baobiao20_add_dynamic_queryDynamic",
            timeout: 100000,
            data: {year:nowYear, month:nowMonth, day:nowDay},
            success: function (data) {
                handle_dynamic_table(data)
            }
        })
    })
}
// dynamic_problem()

var handle_dynamic_table = function (data) {
    var len = data.length
    // 处理均价
    if (len > 1) {
        // 处理合计
        htmlStr = `<tr class="js-add"><td>${data[1]}</td><td>${data[2]}</td></tr>`
        $('.js-dynamic-head').after(htmlStr)
    }
}


// 统一进行请求
contrast()
type_compare()
source01()
price_trend()
sales_destination()
supply()
dynamic_problem()