var nowMonth, nowYear;
var date = new Date();
nowMonth = date.getMonth() + 1;
nowYear = date.getFullYear();
nowDay = date.getDate() - 1;

// report15--来货总量对比
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
                for (let i = 0; i < data[1].length; i++) {
                    dateArr.push(data[1][i][0].slice(5, 10))
                    currentYearData.push(data[1][i][1])
                    lastYearData.push(data[0][i][1])
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

                // 生成折线图
                trend(dateArr, currentYearData, lastYearData)
            }
        })
    })
}
// contrast()

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

// report18--来货类型对比
var type_compare = function () {
  var type1Data = []
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
              
          }
      })
  })
}
type_compare()

// type_compare生成分析文字
var type_compare_analysis = function () {
  var text01 = `<p>2020年12月15日，深圳海吉星市场蔬菜来货总量合计5594吨， 与昨日(5841吨)相比减少247吨，降幅为4%；2020年12月15日，深圳海吉</p><p>星市场蔬菜来货总量合计5594吨， 与昨日(5841吨)相比减少247吨，降幅为4%；</p>`
  var text02 = `1. ${nowYear}年${nowMonth}月${nowDay}日，深圳海吉星市场蔬菜来货总量合计5594吨， 与昨日(5841吨)相比减少247吨，降幅为4%；与${nowYear - 1}年同期(5279吨)相比增加315吨，增幅6%。截止至12月15日23点30分，市场蔬菜档位库存量约为450吨。
                <br/><br/>2. 蔬菜来货品类中，鲜菜类来货4711吨，环比下降2%；硬口类来货883吨，环比下降15%`
  $(function () {
    $('.type_compare_analysis').html(text02)
  })
}
type_compare_analysis()

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


// report16----来源地分析
var source02 = function (source01Title, source02Data) {
  // console.log('source02', source02Data)
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
          }
      })
  })
}
price_trend()

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
sales_destination()

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
  }
}

// 处理下载
var download_supply_table = function () {
  $(function () {
      // 使用outerHTML属性获取整个table元素的HTML代码（包括<table>标签），然后包装成一个完整的HTML文档，设置charset为urf-8以防止中文乱码
      var html = "<html><head><meta charset='utf-8' /></head><body>" + document.getElementsByTagName("table")[1].outerHTML + "</body></html>";
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