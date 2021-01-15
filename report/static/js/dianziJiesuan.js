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
            day = date.getDate();
            dateStr = year + '-' + month;
            // console.log(month, year, day, dateStr);
            $('.date_picker').val(dateStr);
            $('.date_picker').date_input();
            $('.show').click(function () {
                var value = $('.date_picker').val();
                console.log(value);
                var dateArr = value.split('-');
                nowYear = dateArr[0];
                nowMonth = dateArr[1];
                // console.log(dateArr, nowYear, nowMonth);
                baobiao02Fn();
                // shishouFn();
                jiaoyiFn();
                icFn();
                laijiaoFn();
            })
        });

        var baobiao02Fn = function () {
             // 报表
            $(function(){

                var JiesuanData;
                var Data02 = [
                                {"name": "B1", "value": 0},
                                {"name": "B2", "value": 0},
                                {"name": "B3", "value": 0},
                                {"name": "B4", "value": 0},
                                {"name": "B5", "value": 0},
                                {"name": "B6", "value": 0},
                                {"name": "车板固定档", "value": 0}
                             ]
                // 发送ajax请求服务端数据
                $.ajax({
                    type: "get",
                    url:"/baobiao02exer",
                    timeout: 100000,
                    data:{year:nowYear, month:nowMonth},
                    success: function (data) {
                        JiesuanData = data;

                        // var title = nowYear + ' 年 ' + nowMonth + ' 月份蔬菜部电子结算数据分析报表';
                        // $('.title').text(title);

                        // 渲染B1的数据
                        for (var i=0; i < JiesuanData[0].length; i++) {
                            $(".B1").nextAll().eq(i).text(JiesuanData[0][i]);
                        }

                        // 渲染B2的数据
                        for (var i=0; i < JiesuanData[1].length; i++) {
                            $(".B2").nextAll().eq(i).text(JiesuanData[1][i]);
                        }

                        // 渲染B3的数据
                        for (var i=0; i < JiesuanData[2].length; i++) {
                            $(".B3").nextAll().eq(i).text(JiesuanData[2][i]);
                        }

                        // 渲染B4的数据
                        for (var i=0; i < JiesuanData[3].length; i++) {
                            $(".B4").nextAll().eq(i).text(JiesuanData[3][i]);
                        }

                        // 渲染B5的数据
                        for (var i=0; i < JiesuanData[4].length; i++) {
                            $(".B5").nextAll().eq(i).text(JiesuanData[4][i]);
                        }

                        // 渲染B6的数据
                        for (var i=0; i < JiesuanData[5].length; i++) {
                            $(".B6").nextAll().eq(i).text(JiesuanData[5][i]);
                        }

                        // 渲染B7的数据
                        for (var i=0; i < JiesuanData[6].length; i++) {
                            $(".B7").nextAll().eq(i).text(JiesuanData[6][i]);
                        }

                        // 渲染B8的数据
                        for (var i=0; i < JiesuanData[7].length; i++) {
                            $(".B8").nextAll().eq(i).text(JiesuanData[7][i]);
                        }

                        var title = nowYear + ' 年 ' + nowMonth + ' 月份蔬菜部电子结算数据分析报表';
                        $('.title').text(title);

                        shishouFn();

                        // 渲染交易额占比饼图
                        jiaoyiFn(JiesuanData);

                        // 渲染交易额与IC卡刷卡交易对比柱状图
                        icFn(JiesuanData);

                        // 渲染来货量与交易量对比柱状图
                        laihuoFn(JiesuanData);

                        download();
                    },
                    error: function () {
                        alert("服务器繁忙，请再刷新网页！")
                    }
                });
                // 发送ajax请求服务端数据

            });
        };
        baobiao02Fn();

        var shishouFn = function () {
            // 绘制图表id=shishou。
            var shishouTitle = nowYear + ' 年 ' + nowMonth + ' 月份实收金额（IC卡刷卡）占比';
            var shishouData = [
                            {"name": "B1", "value": 0},
                            {"name": "B2", "value": 0},
                            {"name": "B3", "value": 0},
                            {"name": "B4", "value": 0},
                            {"name": "B5", "value": 0},
                            {"name": "B6", "value": 0},
                            {"name": "车板固定档", "value": 0}
                         ];

            echarts.init(document.getElementById('shishou')).setOption({
            title: {
                text: shishouTitle,
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
        shishouFn();


         var jiaoyiFn = function (JiesuanData) {
            // 绘制图表id=jiaoyi。
            var jiaoyiTitle = nowYear + ' 年 ' + nowMonth + ' 月份交易额占比';
            var jiaoyiData = [
                            {"name": "B1", "value": 0},
                            {"name": "B2", "value": 0},
                            {"name": "B3", "value": 0},
                            {"name": "B4", "value": 0},
                            {"name": "B5", "value": 0},
                            {"name": "B6", "value": 0},
                            {"name": "车板固定档", "value": 0}
                         ];

            // 取出交易额的数据
             for (var i=0; i<JiesuanData.length-1; i++) {
                 jiaoyiData[i]["value"] = JiesuanData[i][6]
             }
            echarts.init(document.getElementById('jiaoyi')).setOption({
            title: {
                text: jiaoyiTitle,
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
                data: jiaoyiData,
                label: {
                    normal: {
                        formatter: '{b}:{c}:({d}%)'
                    }
                }
            }
            });
        };


         var icFn = function (JiesuanData) {
                //绘制每日来货车辆数 id=IC
                var ICTitle = nowYear + ' 年 ' + nowMonth + ' 月份蔬菜部交易额与IC卡刷卡交易对比';
                var ICData = [[],[]];
                for (var i=0; i<JiesuanData.length-1; i++) {
                    ICData[0].push(JiesuanData[i][6])
                    ICData[1].push(JiesuanData[i][11])
                }

                var myChart = echarts.init(document.getElementById('IC'));
                var option = {
                        title: {
                            text: ICTitle,
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
                            data : ['交易额', 'IC卡刷卡']
                        },
                        xAxis: {
                            name: '区域',
                            data: ["B1", "B2","B3", "B4","B5", "B6","车板固定档"]
                        },
                        yAxis: {name: '万元'},
                        series: [
                            {
                                type: 'bar',
                                name: '交易额',
                                barWidth: 30,
                                data: ICData[0],
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
                                name: 'IC卡刷卡',
                                barWidth: 30,
                                data: ICData[1],
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


         var laihuoFn = function (JiesuanData) {
                //绘制每日来货车辆数 id=laihuo
                var laihuoTitle = nowYear + ' 年 ' + nowMonth + ' 月份蔬菜部来货量与交易量对比';
                var laihuoData = [[],[]];
                for (var i=0; i<JiesuanData.length-1; i++) {
                    laihuoData[0].push(JiesuanData[i][19])
                    laihuoData[1].push(JiesuanData[i][3])
                }

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
                         //菜单
                        legend : {
                            //菜单字体样式
                            // textStyle : {
                            //     color : 'white'
                            // },
                            //菜单位置
                            x : 'right',
                            //菜单数据
                            data : ['来货量', '交易量']
                        },
                        xAxis: {
                            name: '区域',
                            data: ["B1", "B2","B3", "B4","B5", "B6","车板固定档"]
                        },
                        yAxis: {name: '吨'},
                        series: [
                            {
                                type: 'bar',
                                name: '来货量',
                                barWidth: 30,
                                data: laihuoData[0],
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
                                name: '交易量',
                                barWidth: 30,
                                data: laihuoData[1],
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