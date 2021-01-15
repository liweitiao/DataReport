console.log(123)

$.ajax({
    url: 'http://127.0.0.1:8001/jsonp',
    method: 'get',
    dataType: 'jsonp',
    success: (res) => {
        console.log(res)
    },
    error: () => {
        console.log('error111')
    }

})


$.ajax({
    url: 'http://127.0.0.1:8001/js',
    method: 'get',
    success: (res) => {
        console.log(res)
    },
    error: () => {
        console.log('error222')
    }

})