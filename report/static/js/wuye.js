/**
 * Created by Administrator on 2020/7/30.
 */

var nowMonth, nowYear, nowDate;

var date = new Date();
nowMonth = date.getMonth() + 1;
nowYear = date.getFullYear();
nowDate = date.getDate();

$(function(){
    wuyeFn()
});

var wuyeFn = function () {
     // 报表
    $(function(){
        // 物业档位租赁情况的数据
        var dataWuye = [
            [99, 99, 0, "100.00%", 99, "9172.6", "9172.6", 0, "100.00%"],
            [92, 91, 1, "98.91%", 91, "9167.6", "9121.6", 46, "99.50%"],
            [42, 42, 0, "100.00%", 42, "5497.22", "5497.22", 0, "100.00%"],
            [42, 42, 0, "100.00%", 42, "5514.79", "5514.79", 0, "100.00%"],
            [42, 42, 0, "100.00%", 42, "5514.79", "5514.79", 0, "100.00%"],
            [42, 42, 0, "100.00%", 42, "5497.22", "5497.22", 0, "100.00%"],
            [184, 184, 0, "100.00%", 184, "17161.6", "17161.6", 0, "100.00%"],
            [138, 136, 2, "98.55%", 136, "5156.8", "5132.8", 24, "99.53%"],
            [95, 92, 3, "96.84%", 92, 1780, 1732, 48, "97.30%"],
            [489, 439, 50, "89.78%", 439, "6866.1", "6282.6", "583.5", "91.50%"],
            [1265, 1209, 56, "95.57%", 1209, "71328.72", "70627.22", "701.5", "99.02%"]
        ];

        // 发送ajax请求服务端数据
        $.ajax({
            type: "get",
            url:"/wuye",
            timeout: 100000,
            success: function (data) {
                dataWuye = data;


                // 修改报表标题
                var title = nowYear + ' 年 ' + nowMonth + ' 月 ' + nowDate + ' 日蔬菜管理部物业档位租赁情况';
                $('.title').text(title);

                // 渲染B1的数据
                for (var i=0; i < dataWuye[0].length; i++) {
                    $(".B1").nextAll().eq(i).text(dataWuye[0][i]);
                }

                // 渲染B2的数据
                for (var i=0; i < dataWuye[1].length; i++) {
                    $(".B2").nextAll().eq(i).text(dataWuye[1][i]);
                }

                // 渲染B3的数据
                for (var i=0; i < dataWuye[2].length; i++) {
                    $(".B3").nextAll().eq(i).text(dataWuye[2][i]);
                }

                // 渲染B4的数据
                for (var i=0; i < dataWuye[3].length; i++) {
                    $(".B4").nextAll().eq(i).text(dataWuye[3][i]);
                }

                // 渲染B5的数据
                for (var i=0; i < dataWuye[4].length; i++) {
                    $(".B5").nextAll().eq(i).text(dataWuye[4][i]);
                }

                // 渲染B6的数据
                for (var i=0; i < dataWuye[5].length; i++) {
                    $(".B6").nextAll().eq(i).text(dataWuye[5][i]);
                }

                // 渲染固定档的数据
                for (var i=0; i < dataWuye[6].length; i++) {
                    $(".B7").nextAll().eq(i).text(dataWuye[6][i]);
                }

                // 渲染基地菜的数据
                for (var i=0; i < dataWuye[7].length; i++) {
                    $(".B8").nextAll().eq(i).text(dataWuye[7][i]);
                }

                // 渲染玉米的数据
                for (var i=0; i < dataWuye[8].length; i++) {
                    $(".B9").nextAll().eq(i).text(dataWuye[8][i]);
                }

                // 渲染瓜豆的数据
                for (var i=0; i < dataWuye[9].length; i++) {
                    $(".B10").nextAll().eq(i).text(dataWuye[9][i]);
                }

                // 渲染水菜的数据
                for (var i=0; i < dataWuye[10].length; i++) {
                    $(".B11").nextAll().eq(i).text(dataWuye[10][i]);
                }


                // 渲染蔬菜部物业档位租赁对比柱状图
                Fn01(dataWuye);

                // 渲染蔬菜部物业档位租赁面积对比柱状图
                Fn02(dataWuye);

                // 报表导出功能
                download();
            },
            error: function () {
                alert("服务器繁忙，请再刷新网页！")
            }
        });
        // 发送ajax请求服务端数据

    });
};


 var Fn01 = function (dataWuye) {
        //绘制每日来货车辆数 id=IC
        var Title = nowYear + ' 年 ' + nowMonth + ' 月 ' + nowDate + ' 日蔬菜部物业档位租赁对比（间）';
        var Data = [[],[]];
        for (var i=0; i<dataWuye.length-1; i++) {
            Data[0].push(dataWuye[i][0])
            Data[1].push(dataWuye[i][1])
        }

        var myChart = echarts.init(document.getElementById('Fn01'));
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
                    data : ['可出租', '已出租']
                },
                xAxis: {
                    name: '区域',
                    data: ["B1", "B2","B3", "B4","B5", "B6","冻品区","车板区","综合市场","天光区"]
                },
                yAxis: {name: '间'},
                series: [
                    {
                        type: 'bar',
                        name: '可出租',
                        barWidth: 35,
                        data: Data[0],
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
                        name: '已出租',
                        barWidth: 35,
                        data: Data[1],
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
    };


 var Fn02 = function (dataWuye) {
        //绘制每日来货车辆数 id=IC
        var Title = nowYear + ' 年 ' + nowMonth + ' 月 ' + nowDate + ' 日蔬菜部物业档位租赁面积对比（平方米）';
        var Data = [[],[]];
        for (var i=0; i<dataWuye.length-1; i++) {
            Data[0].push(dataWuye[i][5])
            Data[1].push(dataWuye[i][6])
        }

        var myChart = echarts.init(document.getElementById('Fn02'));
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
                    data : ['可出租面积', '已出租面积']
                },
                xAxis: {
                    name: '区域',
                    data: ["B1", "B2","B3", "B4","B5", "B6","冻品区","车板区","综合市场","天光区"]
                },
                yAxis: {name: '平方米'},
                series: [
                    {
                        type: 'bar',
                        name: '可出租面积',
                        barWidth: 35,
                        data: Data[0],
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
                        name: '已出租面积',
                        barWidth: 35,
                        data: Data[1],
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
    };



var download = function () {
    $(function () {
        // 使用outerHTML属性获取整个table元素的HTML代码（包括<table>标签），然后包装成一个完整的HTML文档，设置charset为urf-8以防止中文乱码
        var html = "<html><head><meta charset='utf-8' /></head><body>" + document.getElementsByTagName("table")[0].outerHTML + "</body></html>";
        // 实例化一个Blob对象，其构造函数的第一个参数是包含文件内容的数组，第二个参数是包含文件类型属性的对象
        var blob = new Blob([html], { type: "application/vnd.ms-excel" });
        // var a = document.getElementsByTagName("a")[0];
        var a = document.getElementsByClassName("download")[0];
        // 利用URL.createObjectURL()方法为a元素生成blob URL
        a.href = URL.createObjectURL(blob);
        // 设置文件名
        var title = $(".title").text() + ".xls";
        a.download = title;
    });
};


