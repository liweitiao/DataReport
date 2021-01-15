/**
 * Created by Administrator on 2020/10/9.
 */
var nowMonth, nowYear, nowDay;
var url = document.referrer
var uri = url.slice(-8)

// 获取cookie的值
var getCookie = function (cookieName) {
    var arrCookie = document.cookie.split(";");
    for(var i = 0; i < arrCookie.length; i++){
        var arr = arrCookie[i].split("=");
        if(cookieName === arr[0].trim()){
            return arr[1];
        }
    }
    return "";
}

// 初始化报表， 判断是否从report06报表中跳转过来
if (uri === 'report06') {
    nowMonth = getCookie('refer_month')
    nowYear= getCookie('refer_year')
    nowDay = getCookie('refer_day')

    $(function () {
        let Str = nowYear + '-' + nowMonth + '-' + nowDay;
        console.log(Str)
        $('.date_picker').val(Str);
        $('.date_picker').date_input();
    })

} else {
    let date = new Date();
    nowMonth = date.getMonth() + 1;
    nowYear = date.getFullYear();
    nowDay = date.getDate();
}

// 设置cookie的值
document.cookie = 'year=' + nowYear
document.cookie = 'month=' + nowMonth
document.cookie = 'day=' + nowDay


// {# 日历时间选择器 #}
$(function(){
    // 初始化时间选择器, 判断是否从report06中跳转过来
    if (uri === 'report06') {
        let month = getCookie('refer_month')
        let year = getCookie('refer_year')
        let day = getCookie('refer_day')
        let dateStr = year + '-' + month + '-' + day;
        // console.log(month, year, day, dateStr);
        $('.date_picker').val(dateStr);
        $('.date_picker').date_input();
    } else {
        let date = new Date();
        let month = date.getMonth() + 1;
        let year = date.getFullYear();
        let day = date.getDate();
        let dateStr = year + '-' + month + '-' + day;
        $('.date_picker').val(dateStr);
        $('.date_picker').date_input();
    }




    $('.show').click(function () {
        var value = $('.date_picker').val();
        var dateArr = value.split('-');

        nowYear = dateArr[0];
        nowMonth = dateArr[1];
        nowDay = dateArr[2];

        document.cookie = 'year=' + nowYear
        document.cookie = 'month=' + nowMonth
        document.cookie = 'day=' + nowDay

    })
});


layui.use('table', function(){
   var table = layui.table;
   //温馨提示：默认由前端自动合计当前行数据。从 layui 2.5.6 开始： 若接口直接返回了合计行数据，则优先读取接口合计行数据。
   //详见：https://www.layui.com/doc/modules/table.html#totalRow
   table.render({
     elem: '#test'
     ,url:'/baobiao08'
     ,toolbar: '#toolbarDemo'
     ,defaultToolbar: ['filter','exports' ]
     ,title: '蔬菜部每日来货清单'
     ,totalRow: true
     ,cols: [[
      //  {type: 'checkbox', fixed: 'left'}
      //  ,{field:'id', title:'ID', width:80, fixed: 'left', unresize: true, sort: true, totalRowText: '合计'}
       {field:'customername', title:'货主名称',width:89}
       ,{field:'doorway', title:'档位号', sort: true, width: 90}
       ,{field:'BI_goodssortna', title:'一级类别', hide: true, width: 80}
       // ,{field:'producttype2', title:'二级类别', hide:true, width: 80}
       // ,{field:'producttype3', title:'三级类别', width: 90}
       ,{field:'productname_xx', title:'商品名称',totalRowText: '合计 : ', width: 90}
       ,{field:'grossweight', title:'毛重', totalRow: true, sort: true, width: 100}
       ,{field:'tareweight', title:'皮重', totalRow: true, sort: true, width: 100}
       ,{field:'netweight', title:'净重', totalRow: true, sort: true, width: 100}
       ,{field:'goodsflagname', title:'来货状态', width: 90}
       ,{field:'vehicletypename', title:'车型', width: 100}
       ,{field:'vehicledesc', title:'车牌号', width: 100}
       ,{field:'grosstime', title:'来货时间', sort: true, width: 180}
       ,{field:'provincecityname', title:'产地'}
       ,{field:'grossoperatorname', title:'操作员', hide:true}
      //  ,{fixed: 'right', title:'操作', toolbar: '#barDemo', width:150}
     ]]
     ,page: true
     ,limit:20
     ,limits:[20, 50, 200, 800]
     ,id: 'testReload'
   });

   var $ = layui.$, active = {
       reload: function () {
           // 执行重载
           table.reload('testReload', {
               url: '/baobiao08'
               ,page: {
                   curr: 1
               }
           }, 'data')
       }
   },
   active02 = {
       reload: function () {
           var doorway = $('#doorway');
           var key = doorway.val().trim()
           // 执行重载
           table.reload('testReload', {
               url: '/baobiao08_searchDoorway'
               ,page: {
                   curr: 1
               }
               ,where: {
                   key: key
               }
           }, 'data')
       }
   },
   active03 = {
       reload: function () {
           var vehicledesc = $('#vehicledesc');
           var key = vehicledesc.val().trim()
           // 执行重载
           table.reload('testReload', {
               url: '/baobiao08_searchVehicledesc'
               ,page: {
                   curr: 1
               }
               ,where: {
                   key: key
               }
           }, 'data')
       }
   },
   active04 = {
       reload: function () {
           var provincecityname = $('#provincecityname');
           var key = provincecityname.val().trim()
           // 执行重载
           table.reload('testReload', {
               url: '/baobiao08_searchProvincecityname'
               ,page: {
                   curr: 1
               }
               ,where: {
                   key: key
               }
           }, 'data')
       }
   },
   active05 = {
       reload: function () {
           var provincecityname = $('#customername');
           var key = provincecityname.val().trim()
           // 执行重载
           table.reload('testReload', {
               url: '/baobiao08_searchCustomername'
               ,page: {
                   curr: 1
               }
               ,where: {
                   key: key
               }
           }, 'data')
       }
   }

   // 按照时间搜索
   $('.dateDiv .show').on('click', function(){
    var type = $(this).data('type');
    active[type] ? active[type].call(this) : '';
  });

   // 搜索档位号
   $('.searchDoorway').on('click', function(){
    var type = $(this).data('type');
    active02[type] ? active02[type].call(this) : '';
  });

   // 搜索车牌号
   $('.searchVehicledesc').on('click', function(){
    var type = $(this).data('type');
    active03[type] ? active03[type].call(this) : '';
  });

   // 搜索产地
   $('.searchProvincecityname').on('click', function(){
    var type = $(this).data('type');
    active04[type] ? active04[type].call(this) : '';
  });

   // 搜索产地
   $('.searchCustomername').on('click', function(){
    var type = $(this).data('type');
    active05[type] ? active05[type].call(this) : '';
  });

   //工具栏事件
   table.on('toolbar(test)', function(obj){
     var checkStatus = table.checkStatus(obj.config.id);
     switch(obj.event){
       case 'getCheckData':
         var data = checkStatus.data;
         layer.alert(JSON.stringify(data));
       break;
       case 'getCheckLength':
         var data = checkStatus.data;
         layer.msg('选中了：'+ data.length + ' 个');
       break;
       case 'isAll':
         layer.msg(checkStatus.isAll ? '全选': '未全选')
       break;
     };
   });
 });