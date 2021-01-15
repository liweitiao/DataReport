/**
 * Created by Administrator on 2020/10/9.
 */

// {# 日历时间选择器 #}
$(function(){
    // 初始化时间选择器, 判断是否从report06中跳转过来
        let date = new Date();
        let month = date.getMonth() + 1;
        let year = date.getFullYear();
        let day = date.getDate();
        let dateStr = year + '-' + month + '-' + day;
        $('.date_picker').val(dateStr);
        $('.date_picker').date_input();


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
     ,url:'/baobiao12'
     ,toolbar: '#toolbarDemo'
     ,defaultToolbar: ['filter','exports' ]
     ,title: '合同更名记录'
     ,totalRow: true
     ,cols: [[
       {field:'shop_id', title:'档位号',width:89}
       ,{field:'rename_time', title:'合同更名日期', width: 160}
       ,{field:'rename_type', title:'变更类型',totalRowText: '合计 : ', width: 120}
       ,{field:'rename_before', title:'变更前名称', totalRow: true, width: 160}
       ,{field:'rename_after', title:'变更后名称', totalRow: true, width: 160}
       ,{field:'relationship', title:'关系', totalRow: true, width: 100}
       ,{field:'remarks', title:'备注'}
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