/**
 * Created by Administrator on 2020/7/30.
 */
// {#初始化页面#}
        var nowMonth, nowYear, nowDay;
        var url = document.referrer
        window.history.back()
        console.log(url)

        var date = new Date();
        nowMonth = date.getMonth() + 1;
        nowYear = date.getFullYear();
        nowDay = date.getDate() - 1;
        // console.log(nowYear, nowMonth);

        document.cookie = 'refer_year=' + nowYear
        document.cookie = 'refer_month=' + nowMonth
        document.cookie = 'refer_day=' + nowDay
        // {# 日历时间选择器 #}
        $(function(){
            date = new Date();
            console.log(date);
            month = date.getMonth() + 1;
            year = date.getFullYear();
            day = date.getDate() - 1;
            dateStr = year + '-' + month + '-' + day;
            console.log(month, year, day, dateStr);
            $('.date_picker').val(dateStr);
            $('.date_picker').date_input();
            $('.show').click(function () {
                var value = $('.date_picker').val();
                // console.log(value);
                var dateArr = value.split('-');
                // console.log(dateArr, nowYear, nowMonth);

                nowYear = dateArr[0];
                nowMonth = dateArr[1];
                nowDay = dateArr[2];

                document.cookie = 'refer_year=' + nowYear
                document.cookie = 'refer_month=' + nowMonth
                document.cookie = 'refer_day=' + nowDay

                baobiaoFn();

            })
        });

        var baobiaoFn = function () {
             // 报表
            $(function(){
                // 每日来货量统计报表的数据
                var dataWuye;

                // 发送ajax请求服务端数据
                $.ajax({
                    type: "get",
                    url:"/baobiao06",
                    timeout: 100000,
                    data:{year:nowYear, month:nowMonth, day:nowDay},
                    success: function (data) {
                        dataWuye = data;


                        // 修改报表标题
                        var title = '蔬菜部档位来货量及过磅金额每日报表';
                        $('.title').text(title);

                        // 修改报表头的日期
                        alertDate(nowYear, nowMonth, nowDay)

                        // 渲染B1的数据
                        for (var i=0; i < dataWuye[0].length; i++) {
                            $(".B").nextAll().eq(i).text(dataWuye[0][i]);
                        }

                        // 渲染B1的数据
                        for (var i=0; i < dataWuye[0].length; i++) {
                            $(".B0").nextAll().eq(i).text(dataWuye[1][i]);
                        }



                        // 渲染B1的数据
                        for (var i=0; i < dataWuye[0].length; i++) {
                            $(".B1").nextAll().eq(i).text(dataWuye[2][i]);
                        }

                        // 渲染B2的数据
                        for (var i=0; i < dataWuye[1].length; i++) {
                            $(".B2").nextAll().eq(i).text(dataWuye[3][i]);
                        }

                        // 渲染B3的数据
                        for (var i=0; i < dataWuye[2].length; i++) {
                            $(".B3").nextAll().eq(i).text(dataWuye[4][i]);
                        }

                        // 渲染B4的数据
                        for (var i=0; i < dataWuye[3].length; i++) {
                            $(".B4").nextAll().eq(i).text(dataWuye[5][i]);
                        }

                        // 渲染B5的数据
                        for (var i=0; i < dataWuye[4].length; i++) {
                            $(".B5").nextAll().eq(i).text(dataWuye[6][i]);
                        }

                        // 渲染B6的数据
                        for (var i=0; i < dataWuye[5].length; i++) {
                            $(".B6").nextAll().eq(i).text(dataWuye[7][i]);
                        }

                        // 渲染固定档的数据
                        for (var i=0; i < dataWuye[6].length; i++) {
                            $(".B7").nextAll().eq(i).text(dataWuye[8][i]);
                        }

                        // 渲染基地菜的数据
                        for (var i=0; i < dataWuye[7].length; i++) {
                            $(".B8").nextAll().eq(i).text(dataWuye[9][i]);
                        }

                        // 渲染玉米的数据
                        for (var i=0; i < dataWuye[8].length; i++) {
                            $(".B9").nextAll().eq(i).text(dataWuye[10][i]);
                        }

                        // 渲染瓜豆的数据
                        for (var i=0; i < dataWuye[9].length; i++) {
                            $(".B10").nextAll().eq(i).text(dataWuye[11][i]);
                        }

                        // 渲染水菜的数据
                        for (var i=0; i < dataWuye[10].length; i++) {
                            $(".B11").nextAll().eq(i).text(dataWuye[12][i]);
                        }

                        // 渲染菇类的数据
                        for (var i=0; i < dataWuye[11].length; i++) {
                            $(".B12").nextAll().eq(i).text(dataWuye[13][i]);
                        }

                        // 渲染固定档的数据
                        for (var i=0; i < dataWuye[12].length; i++) {
                            $(".B13").nextAll().eq(i).text(dataWuye[14][i]);
                        }

                        // 渲染D1/D2的数据
                        for (var i=0; i < dataWuye[13].length; i++) {
                            $(".B14").nextAll().eq(i).text(dataWuye[15][i]);
                        }

                        // 渲染合计的数据
                        for (var i=0; i < dataWuye[14].length; i++) {
                            $(".B15").nextAll().eq(i).text(dataWuye[16][i]);
                        }

                        // 渲染玉米的数据
                        for (var i=0; i < dataWuye[8].length; i++) {
                            $(".B16").nextAll().eq(i).text(dataWuye[17][i]);
                        }

                        // 渲染瓜豆的数据
                        for (var i=0; i < dataWuye[9].length; i++) {
                            $(".B17").nextAll().eq(i).text(dataWuye[18][i]);
                        }

                        // 渲染水菜的数据
                        for (var i=0; i < dataWuye[10].length; i++) {
                            $(".B18").nextAll().eq(i).text(dataWuye[19][i]);
                        }

                        // 渲染菇类的数据
                        for (var i=0; i < dataWuye[11].length; i++) {
                            $(".B19").nextAll().eq(i).text(dataWuye[20][i]);
                        }

                        // 渲染固定档的数据
                        for (var i=0; i < dataWuye[12].length; i++) {
                            $(".B20").nextAll().eq(i).text(dataWuye[21][i]);
                        }

                        // 渲染D1/D2的数据
                        for (var i=0; i < dataWuye[13].length; i++) {
                            $(".B21").nextAll().eq(i).text(dataWuye[22][i]);
                        }

                        // 渲染合计的数据
                        for (var i=0; i < dataWuye[14].length; i++) {
                            $(".B22").nextAll().eq(i).text(dataWuye[23][i]);
                        }

                        // 渲染合计的数据
                        for (var i=0; i < dataWuye[14].length; i++) {
                            $(".B23").nextAll().eq(i).text(dataWuye[24][i]);
                        }



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

        // 修改报表头的日期
        var alertDate = function (year, month, day) {
            $(function () {
                var str01 = '日期: ' + year + ' 年 ' + month + ' 月'
                // 计算出前一天
                var date = new Date(year + '-' + month + '-' + day)
                date.setDate(date.getDate() - 1)
                var yesterday = date.getDate()
                $('.yearAndMonth').text(str01)
                $('.current').text(day + '日')
                $('.yesterday').text(yesterday + '日')
            })
        }

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


