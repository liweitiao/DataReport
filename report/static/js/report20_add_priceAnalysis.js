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

      queryPriceAnalysis(nowYear, nowMonth, nowDay)
  })
});

var queryPriceAnalysis = function (nowYear, nowMonth, nowDay) {
  $(function () {
    $.ajax({
      type: "get",
      url: "/baobiao20_add_priceAnalysis_queryAnalysis",
      timeout: 100000,
      data: {year:nowYear, month:nowMonth, day:nowDay},
      success: function (data) {
        console.log(data)
        if (data.length === 0) {
          //  添加数据
          $('.add').removeAttr('disabled')
          $('.update').attr('disabled', 'disabled')
          //  清空数据
          $('#price')[0].value = null
        } else {
          $('#price')[0].value = data[1]
          // 将id挂到input的属性上
          $('#price').attr('item_id', data[0])
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
  updateButton.addEventListener('click', updateAnalysisFn)
  addButton.addEventListener('click', addAnalysisFn)
})


var addAnalysisFn = function () {
  var newAnalysis = $.trim($('#price')[0].value)
  $.ajax({
    type: "get",
    url:"/baobiao20_add_priceAnalysis_addAnalysis",
    timeout: 100000,
    data: {year:nowYear, month:nowMonth, day:nowDay, newAnalysis: newAnalysis},
    success: function (data) {
      //  清空数据
      $('#price')[0].value = null
      // 将确认修改数据的button禁用
      $('.add').attr('disabled', 'disabled')
      alert("数据添加成功！")
    },
    error: function () {
      alert("服务器繁忙，更新数据失败！")
    }
  })
}



var updateAnalysisFn = function () {
  var newAnalysis = $.trim($('#price')[0].value)
  var item_id = $('#price').attr('item_id')
  $.ajax({
    type: "get",
    url:"/baobiao20_add_priceAnalysis_updateAnalysis",
    timeout: 100000,
    data: {year:nowYear, month:nowMonth, day:nowDay, item_id:item_id, newAnalysis : newAnalysis},
    success: function (data) {
      //  清空数据
      $('#price')[0].value = null
      // 将确认修改数据的button禁用
      $('.update').attr('disabled', 'disabled')
      alert("数据更新成功！")
    },
    error: function () {
      alert("服务器繁忙，更新数据失败！")
    }
  })
}