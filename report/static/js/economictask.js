/**
 * Created by Administrator on 2020/9/7.
 */

// var item;
// item = $("#item_name").val();
// console.log(item);
//
// $("#item_name").change(function(){
//   item = $("#item_name").val();
//   console.log(item)
// });
//  费用项目对应的编号
let item_no;
item_no = $("#item_name").val();
console.log(item_no);

$("#item_name").change(function(){
  item_no = $("#item_name").val();
  console.log(item_no)
});


 // {# 日历时间选择器 #}
        $(function(){
            date = new Date();
            month = date.getMonth() + 1;
            year = date.getFullYear();
            day = date.getDate();
            dateStr = year + '-' + month + '-' + day;
            // console.log(month, year, day, dateStr);
            $('.date_picker').val(dateStr);
            $('.date_picker').date_input();
            $('.show').click(function () {
                let value = $('.date_picker').val();
                let dateArr = value.split('-');

                nowYear = dateArr[0];
                nowMonth = dateArr[1];
                console.log('123', item_no, nowYear, nowMonth)
                queryItem(item_no, nowYear, nowMonth)
            })
        });

        var queryItem = function (item_no, nowYear, nowMonth) {
            $(function () {
                $.ajax({
                    type: "get",
                    url:"/queryItem",
                    timeout: 100000,
                    data: {item_no: item_no, year:nowYear, month:nowMonth},
                    success: function (data) {
                        if (data.length === 0) {
                            //  添加数据
                            $('.add').removeAttr('disabled')
                            $('.update').attr('disabled', 'disabled')
                            clearFn()
                        } else {
                            //  修改数据
                            console.log(data)
                            inputFn(data)
                        }
                    },
                    error: function () {
                        alert("服务器繁忙，请再刷新网页！")
                    }
                })
            })
        }

        var inputFn = function (data) {
            $(function () {
                // 找到select元素，并将查询出来数据的item_id设置属性挂到select上
                $('#item_name').attr('item_id', data[0][0])
                // console.log(select)
                var inputArr = $('.list-input').slice(1, 12)
                for (let i=0; i<inputArr.length; i++) {
                    inputArr[i].value = data[0][i+3]
                }
                $('.update').removeAttr('disabled')
                $('.add').attr('disabled','disabled')
            })
        }

        $(function () {
            let updateButton = $('.update')[0]
            let addButton = $('.add')[0]
            updateButton.addEventListener('click', updateDataFn)
            addButton.addEventListener('click', addDataFn)
        })

        var updateDataFn = function () {
            let item_id = $('#item_name').attr('item_id')
            let item_no = $('#item_name option:selected').val()
            let item_name = $('#item_name option:selected').attr('label')

            console.log(item_id, item_no, item_name)

            let inputArr = $('.list-input').slice(0, 13)

            // 获取全部的list-input的值
            let updateData = []
            for (let i=1; i<inputArr.length; i++) {
                updateData.push($.trim(inputArr[i].value))
            }
            updateData.push($.trim(inputArr[0].value))

            // 将item_id，item_no，item_name添加到updateData之前
            updateData.splice(0, 0, item_name)
            updateData.splice(0, 0, item_no)
            updateData.splice(0, 0, item_id)
            console.log(updateData)

            $.ajax({
                type: "post",
                url:"/updateItem",
                timeout: 100000,
                data: updateData,
                processData: false,
                contentType: false,
                headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                success: function (data) {
                    // 将list-input的数据全部清空
                    clearFn()
                    // 将确认修改数据的button禁用
                    $('.update').attr('disabled', 'disabled')
                    alert("数据更新成功！")
                },
                error: function () {
                    alert("服务器繁忙，更新数据失败！")
                }
            })
        }

        var addDataFn = function () {
            let item_no = $('#item_name option:selected').val()
            let item_name = $('#item_name option:selected').attr('label')

            console.log(item_no, item_name)

            let inputArr = $('.list-input').slice(0, 13)

            // 获取全部的list-input的值
            let addData = []
            for (let i=1; i<inputArr.length; i++) {
                addData.push($.trim(inputArr[i].value))
            }
            addData.push($.trim(inputArr[0].value))

            // 将item_no，item_name添加到updateData之前
            addData.splice(0, 0, item_name)
            addData.splice(0, 0, item_no)
            console.log(addData)

            $.ajax({
                type: "post",
                url:"/addItem",
                timeout: 100000,
                data: addData,
                processData: false,
                contentType: false,
                headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                success: function (data) {
                    // 将list-input的数据全部清空
                    // clearFn()
                    // 将确认修改数据的button禁用
                    // $('.add').attr('disabled', 'disabled')
                    if (data === 200) {
                        clearFn()
                        $('.add').attr('disabled', 'disabled')
                        alert("数据添加成功！123456")
                    }
                    if (data === 400) {
                        alert("该条数据已经存在！")
                    }

                },
                error: function () {
                    alert("服务器繁忙，数据添加失败！")
                }
            })
        }


        var clearFn = function () {
            let inputArr = $('.list-input').slice(0, 13)

            // 获取全部的list-input的值
            for (let i=1; i<inputArr.length; i++) {
                inputArr[i].value = null
            }
        }