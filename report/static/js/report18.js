var nowMonth, nowYear;
var date = new Date();
nowMonth = date.getMonth() + 1;
nowYear = date.getFullYear();
nowDay = date.getDate() - 1;


// {# 日历时间选择器 #}
$(function(){
    date = new Date();
    month = date.getMonth() + 1;
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
        type_compare()
    })
});



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
            }
        })
    })
}
type_compare()
