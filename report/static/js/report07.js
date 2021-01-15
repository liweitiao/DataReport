/**
 * Created by Administrator on 2020/9/22.
 */
var datas  = [];
var nowMonth, nowYear, nowDay;

var date = new Date();
nowMonth = date.getMonth() + 1;
nowYear = date.getFullYear();
nowDay = date.getDate() - 1;

// {# 日历时间选择器 #}
$(function(){
    date = new Date();
    // console.log(date);
    month = date.getMonth() + 1;
    year = date.getFullYear();
    day = date.getDate() - 1;
    dateStr = year + '-' + month + '-' + day;
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
        nowDay = dateArr[2];

        // 先删除id="reportTableDiv"，再创建回来
        updateFn()

        baobiaoFn();

    })
});


var updateFn = function () {
    $('#reportTableDiv').remove()
    var boarddiv = "<div id='reportTableDiv'><table id='reportTable'></table></div>";
    $(document.body).append(boarddiv);
}

var baobiaoFn = function () {
   $(function () {
        $.ajax({
            type: "get",
            url:"/baobiao07",
            timeout: 100000,
            data:{year:nowYear, month:nowMonth, day:nowDay},
            success: function (data) {
                datas = data
                var title = nowYear + ' 年 ' + nowMonth + ' 月 ' + nowDay + ' 日蔬菜部档位来货清单'
                $('.title').text(title);
                Fn(datas)
            },
            error: function () {
                alert("服务器繁忙，请再刷新网页！")
            }
        })
    })
}

baobiaoFn();

var Fn = function (datas) {
    $(function () {
        // $('.bootstrap-table').remove()
        $('#reportTable').bootstrapTable({
            method: 'get',
            cache: false,
            height: 600,
            striped: true,
            pagination: true,
            pageSize: 50,
            pageNumber:1,
            pageList: [20, 50, 100, 200, 500, 1000],
            search: true,
            showColumns: true,
            showRefresh: false,
            showExport: false,
            exportTypes: ['csv','txt','xml'],
            search: true,
            clickToSelect: true,
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            columns:
            [
//				{field:"checked",checkbox:true},
                {field:"customername",title:"货主名称",align:"center",valign:"middle",sortable:"true"},
                {field:"doorway",title:"档位号",align:"center",valign:"middle",sortable:"true"},
                {field:"BI_goodssortna",title:"一级类别",align:"center",valign:"middle",sortable:"true"},
                {field:"producttype2",title:"二级类别",align:"center",valign:"middle",sortable:"true"},
                {field:"producttype3",title:"三级类别",align:"center",valign:"middle",sortable:"true"},
                {field:"productname_xx",title:"商品名称",align:"center",valign:"middle",sortable:"true"},
                {field:"grossweight",title:"毛重",align:"center",valign:"middle",sortable:"true"},
                {field:"tareweight",title:"皮重",align:"center",valign:"middle",sortable:"true"},
                {field:"netweight",title:"净重",align:"center",valign:"middle",sortable:"true"},
                {field:"goodsflagname",title:"来货状态",align:"center",valign:"middle",sortable:"true"},
                {field:"vehicletypename",title:"车型",align:"center",valign:"middle",sortable:"true"},
                {field:"vehicledesc",title:"车牌号",align:"center",valign:"middle",sortable:"true"},
                {field:"grosstime",title:"来货时间",align:"center",valign:"middle",sortable:"true"},
                {field:"provincecityname",title:"产地",align:"center",valign:"middle",sortable:"true"},
                {field:"grossoperatorname",title:"操作员",align:"center",valign:"middle",sortable:"true"}
            ],
            data:datas,
        });
    });
}



// var download = function () {
//             $(function () {
//                 // 使用outerHTML属性获取整个table元素的HTML代码（包括<table>标签），然后包装成一个完整的HTML文档，设置charset为urf-8以防止中文乱码
//                 var html = "<html><head><meta charset='utf-8' /></head><body>" + document.getElementsByTagName("table")[0].outerHTML + "</body></html>";
//                 // 实例化一个Blob对象，其构造函数的第一个参数是包含文件内容的数组，第二个参数是包含文件类型属性的对象
//                 var blob = new Blob([html], { type: "application/vnd.ms-excel" });
//                 // var a = document.getElementsByTagName("a")[0];
//                 var a = document.getElementsByClassName("download")[0];
//                 // 利用URL.createObjectURL()方法为a元素生成blob URL
//                 a.href = URL.createObjectURL(blob);
//                 // 设置文件名
//                 var title = $(".title").text() + ".xls";
//                 a.download = title;
//             });
// };