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

      queryStock(nowYear, nowMonth, nowDay)
  })
});


var queryStock = function (nowYear, nowMonth, nowDay) {
  $(function () {
    $.ajax({
      type: "get",
      url: "/baobiao20_add_queryStock",
      timeout: 100000,
      data: {year:nowYear, month:nowMonth, day:nowDay},
      success: function (data) {
        console.log(data)
        if (data.length === 0) {
          //  添加数据
          $('.add').removeAttr('disabled')
          $('.update').attr('disabled', 'disabled')
          //  清空数据
          $('#amount')[0].value = null
        } else {
          console.log($('#amount'))
          $('#amount')[0].value = data[1]
          // 将id挂到input的属性上
          $('#amount').attr('item_id', data[0])
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
  updateButton.addEventListener('click', updateStockFn)
  addButton.addEventListener('click', addStockFn)
})


var addStockFn = function () {
  var newStock = $.trim($('#amount')[0].value)
  $.ajax({
    type: "get",
    url:"/baobiao20_add_addStock",
    timeout: 100000,
    data: {year:nowYear, month:nowMonth, day:nowDay, newStock: newStock},
    success: function (data) {
      //  清空数据
      $('#amount')[0].value = null
      // 将确认修改数据的button禁用
      $('.add').attr('disabled', 'disabled')
      alert("数据添加成功！")
    },
    error: function () {
      alert("服务器繁忙，更新数据失败！")
    }
  })
}



var updateStockFn = function () {
  var newStock = $.trim($('#amount')[0].value)
  var item_id = $('#amount').attr('item_id')
  // console.log('new----', newStock)

  $.ajax({
    type: "get",
    url:"/baobiao20_add_updateStock",
    timeout: 100000,
    data: {year:nowYear, month:nowMonth, day:nowDay, item_id:item_id, newStock: newStock},
    success: function (data) {
      //  清空数据
      $('#amount')[0].value = null
      // 将确认修改数据的button禁用
      $('.update').attr('disabled', 'disabled')
      alert("数据更新成功！")
    },
    error: function () {
      alert("服务器繁忙，更新数据失败！")
    }
  })
}


// 市场动态及问题
