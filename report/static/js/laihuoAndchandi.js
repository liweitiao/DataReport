/**
 * Created by Administrator on 2020/7/30.
 */
// {#初始化页面#}
        var nowMonth, nowYear;

        var date = new Date();
        nowMonth = date.getMonth();
        nowYear = date.getFullYear();
        // console.log(nowYear, nowMonth);



        // {# 日历时间选择器 #}
        $(function(){
            date = new Date();
            console.log(date);
            month = date.getMonth();
            year = date.getFullYear();
            // day = date.getDate();
            dateStr = year + '-' + month;
            // console.log(month, year, day, dateStr);
            $('.date_picker').val(dateStr);
            $('.date_picker').date_input();
            $('.show').click(function () {
                var value = $('.date_picker').val();
                // console.log(value);
                var dateArr = value.split('-');
                // console.log(dateArr, nowYear, nowMonth);

                nowYear = dateArr[0];
                nowMonth = dateArr[1];
                // var title = nowYear + '年' + nowMonth + '月份蔬菜管理部档位来货量及产地结构信息统计分析报表';
                // $('.title').text(title);

                baobiaoFn();
                chandiFn();
                cheliangFn();
                cheshuFn();
                laihuoFn();
                baobiaoFn();
                // download();
            })
        });

        var baobiaoFn = function () {
             // 报表
            $(function(){
                // 来货量及产地结构信息统计分析报表的数据
                var dataWuye = [
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%'],
                    [6687.29, '40.17%', 74, 336, 176, 117, 703, '72.30%']
                ];

                // 来货车辆车型占比的数据
                var cheliangData = [
                    {"name": "拖头车", "value": 0},
                    {"name": "超大型车", "value": 0},
                    {"name": "大型", "value": 0},
                    {"name": "小型", "value": 0}
                ];
                // 发送ajax请求服务端数据
                $.ajax({
                    type: "get",
                    url:"/baobiao01",
                    timeout: 100000,
                    data:{year:nowYear, month:nowMonth},
                    success: function (data) {
                        dataWuye = data;

                        // 取出来货车辆车型合计数
                        for (var i=0; i<4; i++) {
                            cheliangData[i]["value"] = dataWuye[dataWuye.length -1][i+2]
                        }
                        console.log(cheliangData)

                        // 绘制来货车辆车型占比图表id=cheliang。
                        var cheliangTitle = nowYear + ' 年 ' + nowMonth + ' 月蔬菜区来货车辆车型占比(辆)';
                        cheliangFn(cheliangTitle, cheliangData);

                        // 修改报表标题
                        var title = nowYear + ' 年 ' + nowMonth + ' 月蔬菜管理部档位来货量及产地结构信息统计分析报表';
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

                        // 渲染菇类的数据
                        for (var i=0; i < dataWuye[11].length; i++) {
                            $(".B12").nextAll().eq(i).text(dataWuye[11][i]);
                        }

                        // 渲染固定档的数据
                        for (var i=0; i < dataWuye[12].length; i++) {
                            $(".B13").nextAll().eq(i).text(dataWuye[12][i]);
                        }

                        // 渲染D1/D2的数据
                        for (var i=0; i < dataWuye[13].length; i++) {
                            $(".B14").nextAll().eq(i).text(dataWuye[13][i]);
                        }

                        // 渲染合计的数据
                        for (var i=0; i < dataWuye[14].length; i++) {
                            $(".B15").nextAll().eq(i).text(dataWuye[14][i]);
                        }


                        // 取出来货车辆车型合计数
                        // for (var i=0; i<4; i++) {
                        //     cheliangData[i]["value"] = dataWuye[dataWuye.length -1][i+2]
                        // }


                        // 绘制来货车辆车型占比图表id=cheliang。
                        // var cheliangTitle = nowYear + ' 年 ' + nowMonth + '月蔬菜区来货车辆车型占比(辆)';
                        // cheliangFn(cheliangTitle, cheliangData);


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
        baobiaoFn();



        var cheliangFn = function (cheliangTitle, cheliangData) {
                // 绘制图表id=cheliang。
                echarts.init(document.getElementById('cheliang')).setOption({
                title: {
                    text: cheliangTitle,
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
                    data: cheliangData,
                    label: {
                        normal: {
                            formatter: '{b}:{c}:({d}%)'
                        }
                    }
                }
            });
        };



        var chandiFn = function () {
            // 绘制图表id=chandi。
            var chandiTitle = nowYear + ' 年 ' + nowMonth + ' 月主要蔬菜产地结构';
            var chandiData;
            $(function () {
                //  发送ajax请求数据
                $.ajax({
                    type: "get",
                    url: "/chandi",
                    timeout: 100000,
                    data:{year:nowYear, month:nowMonth},
                    success: function (data) {
                        chandiData = data;
                        echarts.init(document.getElementById('chandi')).setOption({
                            title: {
                                text: chandiTitle,
                                x: 'center'
                            },
                            grid: {
                                width: '160%',
                                right: '5%'
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
                                data: chandiData,
                                label: {
                                    normal: {
                                        formatter: '{b}:{c}:({d}%)'
                                    }
                                }
                            }
                        });
                    },
                    error: function () {
                        alert("请求产地结构数据失败，请再刷新网页！")
                    }
                });


            });

        };
        chandiFn();


        var cheshuFn = function () {
                //绘制每日来货车辆数 id=cheshu
                var cheshuTitle = nowYear + ' 年 ' + nowMonth + ' 月蔬菜区每日来货车辆数（辆）';
                var cheshuData = [4300, 5203, 6326, 4103, 5140, 5250, 6260, 5130, 4120, 4220];

                $(function () {
                    $.ajax({
                        type: "get",
                        url: "/cheshu",
                        timeout: 100000,
                        data:{year:nowYear, month:nowMonth},
                        success: function (data) {
                            cheshuData = data;
                            var myChart = echarts.init(document.getElementById('cheshu'));
                            var option = {
                                    title: {
                                        text: cheshuTitle,
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
                                        name: '日',
                                        data: ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"
                                                ,"17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
                                    },
                                    yAxis: {name:'辆'},
                                    series: [
                                        {
                                            type: 'bar',
                                            barWidth: 10,
                                            data: cheshuData,
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
                        },
                        error: function () {
                            alert("请求每日来货车辆数失败，请再刷新网页！")
                        }
                    });

                });

        };
        cheshuFn();


        var laihuoFn = function () {
            //绘制每日来货车辆数id=laihuo
            var laihuoTitle = nowYear + ' 年 ' + nowMonth + ' 月蔬菜每日来货量（吨/日）';
            var laihuoData;

            $(function () {
                $.ajax({
                    type: "get",
                    url: "/laihuo",
                    timeout: 100000,
                    data:{year:nowYear, month:nowMonth},
                    success: function (data) {
                        laihuoData = data;
                        var myChart = echarts.init(document.getElementById('laihuo'));
                        var option = {
                                title: {
                                    text: laihuoTitle,
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
                                    name: '日',
                                    data: ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"
                                            ,"17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
                                },
                                yAxis: {name: '吨'},
                                series: [
                                    {
                                        type: 'bar',
                                        barWidth: 10,
                                        data: laihuoData,
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
                    },
                    error: function () {
                        alert("请求每日来货量失败，请再刷新网页！")
                    }
                });

            });
        };
        var laihuoFn02 = function () {
            //绘制每日来货车辆数id=laihuo
            var laihuoTitle = nowYear + ' 年 ' + nowMonth + ' 月蔬菜每日来货量（吨/日）';
            var myChart02 = echarts.init(document.getElementById('laihuo'));
            var dataArr02 = [430, 520, 636, 410, 510, 520, 620, 510, 410, 420];

            var option02 = {
                    title: {
                        text: laihuoTitle,
                        left:'center'
                    },
                    tooltip: {},
                    xAxis: {
                        data: ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"
                                ,"17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
                    },
                    yAxis: {},
                    series: [
                        {
                            name: '可出租',
                            type: 'bar',
                            barWidth: 10,
                            data: dataArr02,
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
            myChart02.setOption(option02);
        };
        laihuoFn();

        var download = function () {
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
                var title = $(".title").text() + ".xls";
                a.download = title;
            });
        };

        // $(window).load(function () {
        //    download();
        // });

        // window.onload = function () {
        //     download();
        // };


