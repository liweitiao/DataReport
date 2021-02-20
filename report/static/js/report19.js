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
        supply()
    })
});


// 供应情况
var supply = function () {
    $(function () {
        $.ajax({
            type: "get",
            url: "baobiao19_supply",
            timeout: 100000,
            data: {year:nowYear, month:nowMonth, day:nowDay},
            success: function (data) {
                console.log(data)
                handle(data)
            }
        })
    })
}
supply()

// 生成表格
var handle = function (data) {
    var len = data.length
    // 处理均价
    if (len > 1) {
        var sum = data.pop()
        // 处理合计
        htmlStr = `<tr class="js-add"><td colspan="3">合计</td><td>${sum[0]}</td><td>${sum[1]}</td></tr>`
        $('.js-head').after(htmlStr)

        // 处理其它
        len = data.length
        for (let i = len - 1; i >= 0; i--) {
            htmlStr = `<tr class="js-add"><td>${i + 1}</td><td>${data[i][0]}</td><td>${data[i][1]}</td><td>${data[i][2]}</td><td>${data[i][3]}</td></tr>`
            $('.js-head').after(htmlStr)
        }
        download()
    }
}


// 将全部add的元素删除
var removeAdd = function () {
    $('.js-add').remove()
  }

// 处理下载
var download = function () {
    $(function () {
        // 使用outerHTML属性获取整个table元素的HTML代码（包括<table>标签），然后包装成一个完整的HTML文档，设置charset为urf-8以防止中文乱码
        var html = "<html><head><meta charset='utf-8' /></head><body>" + document.getElementsByTagName("table")[0].outerHTML + "</body></html>";
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