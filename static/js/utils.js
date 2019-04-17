

var log = function() {
    console.log.apply(console, arguments)
}

var e = function(sel) {
    return document.querySelector(sel)
}

/*
 ajax 函数
 ajax 的跨域, 只能请求localhost:3000的
*/
var ajax = function(method, path, data, responseCallback) {
    /**
     * 该函数调用时，
     * 前端使用method 方法请求服务器的path路径，请求时候的body内容为data
     * 当服务器响应该请求时，会返回json数据
     * 前端接收到响应时，才会调用回掉函数responseCallback来处理返回的json数据
     */
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    // 这个不是必须的
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            responseCallback(r.response)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}


// 向服务器发送训练请求
var apiTrain = function(form, callback) {
    var path = '/api/borrow'
    // 在 ajax 完成之后，才会调用函数 callback
    // 回调函数在 ajax 中传入的参数是 r.response
    ajax('POST', path, form, callback)
}




