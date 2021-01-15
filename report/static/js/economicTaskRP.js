/**
 * Created by Administrator on 2020/7/30.
 */
// {#初始化页面#}
        var nowMonth, nowYear;
        var date = new Date();
        nowMonth = date.getMonth();
        nowYear = date.getFullYear();

        // {# 日历时间选择器 #}
        $(function(){
            date = new Date();
            console.log(date);
            month = date.getMonth();
            year = date.getFullYear();
            day = date.getDate();
            dateStr = year + '-' + month;

            $('.date_picker').val(dateStr);
            $('.date_picker').date_input();
            $('.show').click(function () {
                var value = $('.date_picker').val();

                var dateArr = value.split('-');

                nowYear = dateArr[0];
                nowMonth = dateArr[1];

                economicFn();
            })
        });

        var economicFn = function () {
             // 报表
            $(function(){
                // 经济任务明细表的数据
                var dataEconomic;

                // 欠费责任区域报表的数据
                var dataQianfei = [[],[],[],[],[],[],[],[],[],[],[]]

                // 各项费用实收占比的数据
                var shishouData = [
                    {"name": "大档佣金", "value": 0},
                    {"name": "大档管理费", "value": 0},
                    {"name": "阁楼租金", "value": 0},
                    {"name": "仓库租金", "value": 0},
                    {"name": "车板租金", "value": 0},
                    {"name": "过磅费", "value": 0},
                    {"name": "违约金", "value": 0},
                    {"name": "冻品管理费", "value": 0},
                    {"name": "地摊租金", "value": 0},
                    {"name": "综合市场场地租金", "value": 0}
                ];
                // 发送ajax请求服务端数据
                $.ajax({
                    type: "get",
                    url:"/economicTask",
                    timeout: 100000,
                    data:{year:nowYear, month:nowMonth},
                    success: function (data) {
                        dataEconomic = data;
                        console.log(data)

                        // 取出欠费责任区域报表的数据
                        for (let i=0; i<dataEconomic.length; i++) {
                            dataQianfei[i].push(dataEconomic[i][4])
                            dataQianfei[i].push(dataEconomic[i][5])
                            dataQianfei[i].push(dataEconomic[i][10])
                        }

                        // 渲染欠费责任区域报表的数据
                        qianfeiFn(dataQianfei);

                        // 取出各项费用实收占比数据
                        for (var i=0; i<10; i++) {
                            shishouData[i]["value"] = dataEconomic[i][12]
                        }

                        // 绘制各项费用实收占比图表id=Shishou。
                        var shishouTitle = nowYear + ' 年 ' + nowMonth + ' 月份蔬菜管理部各项费用实收占比';
                        shishouFn(shishouTitle, shishouData);

                        // 渲染柱状图
                        shouruFn(dataEconomic);

                        // 修改报表标题
                        var title = nowYear + ' 年 ' + nowMonth + ' 月份蔬菜管理部公司经济任务完成情况明细表';
                        $('.title').text(title);

                        // 渲染大档佣金的数据
                        for (var i=0; i < dataEconomic[0].length; i++) {
                            $(".B1").nextAll().eq(i).text(dataEconomic[0][i+3]);
                        }

                        // 渲染大档管理费的数据
                        for (var i=0; i < dataEconomic[1].length; i++) {
                            $(".B2").nextAll().eq(i).text(dataEconomic[1][i+3]);
                        }

                        // 渲染阁楼租金的数据
                        for (var i=0; i < dataEconomic[2].length; i++) {
                            $(".B3").nextAll().eq(i).text(dataEconomic[2][i+3]);
                        }

                        // 渲染仓库租金的数据
                        for (var i=0; i < dataEconomic[3].length; i++) {
                            $(".B4").nextAll().eq(i).text(dataEconomic[3][i+3]);
                        }

                        // 渲染车板租金的数据
                        for (var i=0; i < dataEconomic[4].length; i++) {
                            $(".B5").nextAll().eq(i).text(dataEconomic[4][i+3]);
                        }

                        // 渲染过磅费的数据
                        for (var i=0; i < dataEconomic[5].length; i++) {
                            $(".B6").nextAll().eq(i).text(dataEconomic[5][i+3]);
                        }

                        // 渲染违约金的数据
                        for (var i=0; i < dataEconomic[6].length; i++) {
                            $(".B7").nextAll().eq(i).text(dataEconomic[6][i+3]);
                        }

                        // 渲染冻品管理费的数据
                        for (var i=0; i < dataEconomic[7].length; i++) {
                            $(".B8").nextAll().eq(i).text(dataEconomic[7][i+3]);
                        }

                        // 渲染地摊租金的数据
                        for (var i=0; i < dataEconomic[8].length; i++) {
                            $(".B9").nextAll().eq(i).text(dataEconomic[8][i+3]);
                        }

                        // 渲染综合市场场地租金的数据
                        for (var i=0; i < dataEconomic[9].length; i++) {
                            $(".B10").nextAll().eq(i).text(dataEconomic[9][i+3]);
                        }

                        // 渲染合计的数据
                        for (var i=0; i < dataEconomic[10].length; i++) {
                            $(".B11").nextAll().eq(i).text(dataEconomic[10][i+3]);
                        }

                        // 取出欠费责任区域报表的数据
                        // for (let i=0; i<dataEconomic.length; i++) {
                        //     dataQianfei[i].push(dataEconomic[i][4])
                        //     dataQianfei[i].push(dataEconomic[i][5])
                        //     dataQianfei[i].push(dataEconomic[i][10])
                        // }
                        // 渲染欠费责任区域报表的数据
                        // qianfeiFn(dataQianfei);

                        // 绘制各项费用实收占比图表id=Shishou。
                        // var shishouTitle = nowYear + ' 年 ' + nowMonth + ' 月份蔬菜管理部各项费用实收占比';
                        // shishouFn(shishouTitle, shishouData);
                        //
                        // // 渲染柱状图
                        // shouruFn(dataEconomic);

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
        economicFn();


        var qianfeiFn = function (dataQianfei) {
            // 渲染大档佣金的数据
            for (var i=0; i < dataQianfei[0].length; i++) {
                $(".Q1").nextAll().eq(i+1).text(dataQianfei[0][i]);
            }

            // 渲染大档管理费的数据
            for (var i=0; i < dataQianfei[1].length; i++) {
                $(".Q2").nextAll().eq(i+1).text(dataQianfei[1][i]);
            }

            // 渲染阁楼租金的数据
            for (var i=0; i < dataQianfei[2].length; i++) {
                $(".Q3").nextAll().eq(i+1).text(dataQianfei[2][i]);
            }

            // 渲染仓库租金的数据
            for (var i=0; i < dataQianfei[3].length; i++) {
                $(".Q4").nextAll().eq(i+1).text(dataQianfei[3][i]);
            }

            // 渲染车板租金的数据
            for (var i=0; i < dataQianfei[4].length; i++) {
                $(".Q5").nextAll().eq(i+1).text(dataQianfei[4][i]);
            }

            // 渲染过磅费的数据
            for (var i=0; i < dataQianfei[5].length; i++) {
                $(".Q6").nextAll().eq(i+1).text(dataQianfei[5][i]);
            }

            // 渲染违约金的数据
            for (var i=0; i < dataQianfei[6].length; i++) {
                $(".Q7").nextAll().eq(i+1).text(dataQianfei[6][i]);
            }

            // 渲染冻品管理费的数据
            for (var i=0; i < dataQianfei[7].length; i++) {
                $(".Q8").nextAll().eq(i+1).text(dataQianfei[7][i]);
            }

            // 渲染地摊租金的数据
            for (var i=0; i < dataQianfei[8].length; i++) {
                $(".Q9").nextAll().eq(i+1).text(dataQianfei[8][i]);
            }

            // 渲染综合市场场地租金的数据
            for (var i=0; i < dataQianfei[9].length; i++) {
                $(".Q10").nextAll().eq(i+1).text(dataQianfei[9][i]);
            }

            // 渲染合计的数据
            for (var i=0; i < dataQianfei[10].length; i++) {
                $(".Q11").nextAll().eq(i).text(dataQianfei[10][i]);
            }

            // 报表导出功能
            download02();
        }


        var shishouFn = function (cheliangTitle, shishouData) {
                // 绘制图表id=Shishou。
                echarts.init(document.getElementById('Shishou')).setOption({
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
                    data: shishouData,
                    label: {
                        normal: {
                            formatter: '{b}:{c}:({d}%)'
                        }
                    }
                }
            });
        };


        var shouruFn = function (dataEconomic) {
                //绘制每日来货车辆数 id=Shouru
                let Title = nowYear + ' 年 ' + nowMonth + ' 月份蔬菜部收入情况（元）';
                let Data = [[],[]];
                for (let i=0; i<dataEconomic.length-1; i++) {
                    Data[0].push(dataEconomic[i][5])
                    Data[1].push(dataEconomic[i][10])
                }

                var myChart = echarts.init(document.getElementById('Shouru'));
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
                            data : ['累计实收', '累计欠费']
                        },
                        xAxis: {
                            name: '项目',
                            data: ["大档佣金","大档管理费","阁楼租金","仓库租金","车板租金","过磅费","违约金","冻品管理费","地摊租金","综合市场"],
                            "axisLabel": {
                            interval:0
                        }
                        },
                        yAxis: {name: '元'},
                        series: [
                            {
                                type: 'bar',
                                name: '累计实收',
                                barWidth: 20,
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
                                name: '累计欠费',
                                barWidth: 20,
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


        var download02 = function () {
            $(function () {
                // 使用outerHTML属性获取整个table元素的HTML代码（包括<table>标签），然后包装成一个完整的HTML文档，设置charset为urf-8以防止中文乱码
                var html = "<html><head><meta charset='utf-8' /></head><body>" + document.getElementsByTagName("table")[2].outerHTML + "</body></html>";
                // 实例化一个Blob对象，其构造函数的第一个参数是包含文件内容的数组，第二个参数是包含文件类型属性的对象
                var blob = new Blob([html], { type: "application/vnd.ms-excel" });
                // var a = document.getElementsByTagName("a")[0];
                var a = document.getElementsByClassName("download")[1];
                // 利用URL.createObjectURL()方法为a元素生成blob URL
                a.href = URL.createObjectURL(blob);
                // 设置文件名
                var title = $(".title02").text() + ".xls";
                a.download = title;
            });
        };


