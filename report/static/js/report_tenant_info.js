// 搜索的字段
var name, idNo

$(function(){
  $('.js-search-name').on('click', function() {
    name = $('.js-name').val().trim()
    idNo = 'xxxx'
    removeAdd()
    social_info(name, idNo)
    honor_info(name, idNo)
    management_info(name, idNo)
    contract_record(name, idNo)
    tenant_information(name, idNo)
    tenant_contract(name, idNo)
    employee_information(name, idNo)
    penal(name, idNo)
    goods(name, idNo)
    parking_card(name, idNo)

      setTimeout(()=>{
    console.log('download');
    download()
  }, 15000)
  })

  $('.js-search-id').on('click', function() {
    idNo = $('.js-id').val().trim()
    name = 'xxxx'
    removeAdd()
    social_info(name, idNo)
    honor_info(name, idNo)
    management_info(name, idNo)
    contract_record(name, idNo)
    tenant_information(name, idNo)
    tenant_contract(name, idNo)
    employee_information(name, idNo)
    penal(name, idNo)
    goods(name, idNo)
    parking_card(name, idNo)

    setTimeout(()=>{
    console.log('download');
    download()
  }, 15000)
  })


})


// 查询社会关系
var social_info = function (name, idNo) {
  $(function () {
    $.ajax({
      type: "get",
      url: "http://127.0.0.1:8000/social_info",
      timeout: 10000,
      data: {name: name, idNo: idNo},
      success: function (data) {
        for (var i=0; i<data.length; i++) {
          for (var j = 0; j < data[i].length; j++) {
            data[i][j] = data[i][j] !== null ? data[i][j] : ''
          }
          htmlStr = `<tr class="js-add"><td>${data[i][0]}</td><td>${data[i][1] + ','}</td><td>${data[i][2]}</td><td>${data[i][3]}</td><td>${data[i][4]}</td><td>${data[i][5]}</td><td>${data[i][6]}</td><td>${data[i][7]}</td><td></td><td></td></tr>`
          $('.js-social_info').after(htmlStr)
        }
      },
      error: function () {
        alert("服务器获取社会关系出错， 请重新请求数据！")
    }
    })
  })
}


// 查询会员荣誉
var honor_info = function (name, idNo) {
  $(function () {
    $.ajax({
      type: "get",
      url: "http://127.0.0.1:8000/honor_info",
      timeout: 10000,
      data: {name: name, idNo: idNo},
      success: function (data) {
        for (var i=0; i<data.length; i++) {
          for (var j = 0; j < data[i].length; j++) {
            data[i][j] = data[i][j] !== null ? data[i][j] : ''
          }
          htmlStr = `<tr class="js-add"><td>${data[i][0]}</td><td>${data[i][1] + ','}</td><td>${data[i][2]}</td><td>${data[i][3]}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>`
          $('.js-honor_info').after(htmlStr)
        }
      },
      error: function () {
        alert("服务器获取会员荣誉出错， 请重新请求数据！")
    }
    })
  })
}


// 查询经营信息
var management_info = function (name, idNo) {
  $(function () {
    $.ajax({
      type: "get",
      url: "http://127.0.0.1:8000/management_info",
      timeout: 10000,
      data: {name: name, idNo: idNo},
      success: function (data) {
        for (var i=0; i<data.length; i++) {
          for (var j = 0; j < data[i].length; j++) {
            data[i][j] = data[i][j] !== null ? data[i][j] : ''
          }
          htmlStr = `<tr class="js-add"><td>${data[i][0]}</td><td>${data[i][1]}</td><td>${data[i][2]}</td><td>${data[i][3]}</td><td>${data[i][4]}</td><td>${data[i][5]}</td><td>${data[i][6]}</td><td>${data[i][7]}</td><td>${data[i][8]}</td><td></td></tr>`
          $('.js-management_info').after(htmlStr)
        }
      },
      error: function () {
        alert("服务器获取经营信息出错， 请重新请求数据！")
    }
    })
  })
}


// 查询合同更名记录
var contract_record = function (name, idNo) {
  $(function () {
    $.ajax({
      type: "get",
      url: "http://127.0.0.1:8000/contract_record",
      timeout: 10000,
      data: {name: name, idNo: idNo},
      success: function (data) {
        for (var i=0; i<data.length; i++) {
          for (var j = 0; j < data[i].length; j++) {
            data[i][j] = data[i][j] !== null ? data[i][j] : ''
          }
          htmlStr = `<tr class="js-add"><td>${data[i][0]}</td><td>${data[i][1]}</td><td>${data[i][2]}</td><td>${data[i][3]}</td><td>${data[i][4]}</td><td>${data[i][5]}</td><td>${data[i][6]}</td><td></td><td></td><td></td></tr>`
          $('.js-contract_record').after(htmlStr)
        }
      },
      error: function () {
        alert("服务器获取合同更名记录出错， 请重新请求数据！")
    }
    })
  })
}


// 查询承租人的信息
var tenant_information = function (name, idNo) {
  $(function () {
    $.ajax({
      type: "get",
      url: "http://127.0.0.1:8000/tenant_information",
      timeout: 10000,
      data: {name: name, idNo: idNo},
      success: function (data) {
        for (var i = 0; i < data.length; i++) {
          data[i] = data[i] !== null ? data[i] : '/'
        }
        htmlStr = `<tr class="js-add"><td>${data[0]}</td><td>${data[1] + ','}</td><td>${data[2]}</td><td>${data[3]}</td><td>${data[4]}</td><td>${data[5]}</td><td>${data[6]}</td><td>${data[7]}</td><td>${data[8]}</td><td></td></tr>`
        $('.js-tenant').after(htmlStr)
      },
      error: function () {
        alert("服务器获取承租人的信息出错， 请重新请求数据！")
    }
    })
  })
}


// 查询合同物业的信息
var tenant_contract = function (name, idNo) {
  $(function () {
    $.ajax({
      type: "get",
      url: "http://127.0.0.1:8000/tenant_contract",
      timeout: 10000,
      data: {name: name, idNo: idNo},
      success: function (data) {
        for (var i=0; i<data.length; i++) {
          htmlStr = `<tr class="js-add"><td>${data[i][0]}</td><td>${data[i][1]}</td><td>${data[i][2]}</td><td>${data[i][3]}</td><td>${data[i][4]}</td><td>${data[i][5]}</td><td></td><td></td><td></td><td></td></tr>`
          $('.js-contract').after(htmlStr)
        }
      },
      error: function () {
        alert("服务器获取承租物业信息出错， 请重新请求数据！")
    }
    })
  })
}


// 查询从业人员信息
var employee_information = function (name, idNo) {
  $(function () {
    $.ajax({
      type: "get",
      url: "http://127.0.0.1:8000/employee_information",
      timeout: 10000,
      data: {name: name, idNo: idNo},
      success: function (data) {
        for (var i=0; i<data.length; i++) {
          htmlStr = `<tr class="js-add"><td>${data[i][0]}</td><td>${data[i][1] + ','}</td><td>${data[i][2]}</td><td>${data[i][3]}</td><td>${data[i][4]}</td><td>${data[i][5]}</td><td>${data[i][6]}</td><td>${data[i][7]}</td><td>${data[i][8]}</td><td>${data[i][9]}</td></tr>`
          $('.js-employee').after(htmlStr)
        }
      },
      error: function () {
        alert("服务器获取承租物业信息出错， 请重新请求数据！")
    }
    })
  })
}


// 查询罚单
/**
 * 
 * @param {string} name 搜索的商户名字
 * @param {string} idNo 搜索的商户档位号
*/
var penal = function (name, idNo) {
  $(function () {
    $.ajax({
      type: "get",
      url: "http://127.0.0.1:8000/penal",
      timeout: 10000,
      data: {name: name, idNo: idNo},
      success: function (data) {
        for (var i=0; i<data.length; i++) {
          for (var j = 0; j < data[i].length; j++) {
            data[i][j] = data[i][j] !== null ? data[i][j] : ''
          }
          htmlStr = `<tr class="js-add"><td>${data[i][0]}</td><td>${data[i][1]}</td><td colspan="3">${data[i][2]}</td><td>${data[i][3]}</td><td>${data[i][4]}</td><td></td><td></td><td></td></tr>`
          $('.js-penal').after(htmlStr)
        }
      },
      error: function () {
        alert("服务器获取罚单信息出错， 请重新请求数据！")
    }
    })
  })
}


// 查询来货情况
var goods = function (name, idNo) {
  $(function () {
    $.ajax({
      type: "get",
      url: "http://127.0.0.1:8000/goods",
      timeout: 80000,
      data: {name: name, idNo: idNo},
      success: function (data) {
        for (var i=0; i<data.length; i++) {
          htmlStr = `<tr class="js-add"><td>${data[i][0]}</td><td>${data[i][1]}</td><td colspan="4">${data[i][2]}</td><td colspan="4">${data[i][3]}</td></tr>`
          $('.js-goods').after(htmlStr)
        }
      },
      error: function () {
        alert("服务器获取罚单信息出错， 请重新请求数据！")
    }
    })
  })
}


// 查询停车卡
var parking_card= function (name, idNo) {
  $(function () {
    $.ajax({
      type: "get",
      url: "http://127.0.0.1:8000/parking_card",
      timeout: 80000,
      data: {name: name, idNo: idNo},
      success: function (data) {
        for (var i=0; i<data.length; i++) {
          htmlStr = `<tr class="js-add"><td>${data[i][0]}</td><td>${data[i][1]}</td><td>${data[i][2]}</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>`
          $('.js-parkingCard').after(htmlStr)
        }
      },
      error: function () {
        alert("服务器获取罚单信息出错， 请重新请求数据！")
    }
    })
  })
}



// 将全部add的元素删除
var removeAdd = function () {
  $('.js-add').remove()
}

// 导出报表
var download = function () {
  $(function () {
      // 使用outerHTML属性获取整个table元素的HTML代码（包括<table>标签），然后包装成一个完整的HTML文档，设置charset为urf-8以防止中文乱码
      var html = "<html><head><meta charset='utf-8' /></head><body>" + document.getElementsByTagName("table")[0].outerHTML + "</body></html>";
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