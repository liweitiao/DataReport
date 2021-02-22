// {# 日历时间选择器 #}
$(function(){
  date = new Date();
  month = date.getMonth() + 1;
  year = date.getFullYear();
  day = date.getDate();
  dateStr = year + '-' + month + '-' + day;
  $('.date_picker').val(dateStr);
  $('.date_picker').date_input();
  $('.show').click(function () {
      let value = $('.date_picker').val();
      let dateArr = value.split('-');

      nowYear = dateArr[0];
      nowMonth = dateArr[1];
      nowDay = dateArr[2];

      queryDynamic_Problem(nowYear, nowMonth, nowDay)
  })
});

var queryDynamic_Problem = function (nowYear, nowMonth, nowDay) {
  $(function () {
    $.ajax({
      type: "get",
      url: "/baobiao20_add_dynamic_queryDynamic",
      timeout: 100000,
      data: {year:nowYear, month:nowMonth, day:nowDay},
      success: function (data) {
        console.log(data)
        if (data.length === 0) {
          //  添加数据
          $('.add').removeAttr('disabled')
          $('.update').attr('disabled', 'disabled')
          //  清空数据
          $('#dynamic')[0].value = null
          $('#problem')[0].value = null
        } else {
          $('#dynamic')[0].value = data[1]
          $('#problem')[0].value = data[2]
          // 将id挂到input的属性上
          $('#dynamic').attr('item_id', data[0])
          $('.update').removeAttr('disabled')
          $('.add').attr('disabled','disabled')
        }
      }
    })
  })
}


// 添加事件
$(function () {
  let updateButton = $('.update')[0]
  let addButton = $('.add')[0]
  updateButton.addEventListener('click', updateDynamicFn)
  addButton.addEventListener('click', addDynamicFn)
})


var addDynamicFn = function () {
  var newDynamic = $.trim($('#dynamic')[0].value)
  var newProblem = $.trim($('#problem')[0].value)
  $.ajax({
    type: "get",
    url:"/baobiao20_add_dynamic_addDynamic",
    timeout: 100000,
    data: {year:nowYear, month:nowMonth, day:nowDay, newDynamic: newDynamic, newProblem: newProblem},
    success: function (data) {
      //  清空数据
      $('#dynamic')[0].value = null
      $('#problem')[0].value = null
      // 将确认修改数据的button禁用
      $('.add').attr('disabled', 'disabled')
      alert("数据添加成功！")
    },
    error: function () {
      alert("服务器繁忙，更新数据失败！")
    }
  })
}



var updateDynamicFn = function () {
  var newDynamic = $.trim($('#dynamic')[0].value)
  var newProblem = $.trim($('#problem')[0].value)
  var item_id = $('#dynamic').attr('item_id')
  // console.log('new----', newStock)

  $.ajax({
    type: "get",
    url:"/baobiao20_add_dynamic_updateDynamic",
    timeout: 100000,
    data: {year:nowYear, month:nowMonth, day:nowDay, item_id:item_id, newDynamic: newDynamic, newProblem: newProblem},
    success: function (data) {
      //  清空数据
      $('#dynamic')[0].value = null
      $('#problem')[0].value = null
      // 将确认修改数据的button禁用
      $('.update').attr('disabled', 'disabled')
      alert("数据更新成功！")
    },
    error: function () {
      alert("服务器繁忙，更新数据失败！")
    }
  })
}