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
        
        removeAdd()
        price_trend()
    })
});

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
        $('.js-head').after(htmlStr) 

        // 处理其它
        for (let i = 0; i < data02.length - 1; i++) {
            htmlStr = `<tr class="js-add"><td>${data02[i][0]}</td><td>${data02[i][1]}</td><td>${data02[i][2]}</td><td>${data02[i][3]}</td><td>${data02[i][4]}</td></tr>`
            $('.js-head').after(htmlStr)
        }
        download_price_table()
    }
}


// 将全部add的元素删除
var removeAdd = function () {
    $('.js-add').remove()
  }

// 处理下载
var download_price_table = function () {
    $(function () {
        // 使用outerHTML属性获取整个table元素的HTML代码（包括<table>标签），然后包装成一个完整的HTML文档，设置charset为urf-8以防止中文乱码
        var html = "<html><head><meta charset='utf-8' /></head><body>" + document.getElementsByTagName("table")[1].outerHTML + "</body></html>";
        // 实例化一个Blob对象，其构造函数的第一个参数是包含文件内容的数组，第二个参数是包含文件类型属性的对象
        var blob = new Blob([html], { type: "application/vnd.ms-excel" });
        // var a = document.getElementsByTagName("a")[0];
        var a = document.getElementsByClassName("download")[0];
        // 利用URL.createObjectURL()方法为a元素生成blob URL
        a.href = URL.createObjectURL(blob);
        // 设置文件名
        var title = "蔬菜价格统计" + ".xls";
        a.download = title;
    });
};