var bindEventShowClick = function () {
    // 所以我们先找到 id-show-all 按钮, 给其绑定click 事件
    var button = e('#id-show-all')

    button.addEventListener('click', function (event) {

        var books = e('#book-list')

        apiGetAllRecord('', function (status, r) {
            log('r: ', r)
            var o = JSON.parse(r)
            log("o:", o)
            //动态创建表格 
            for (var i = 0; i < o.length; i++) {
                record = o[i]
                var trNode = books.insertRow();
                var returned = "未归还"
                if (record.deleted) {
                    returned = "已归还"
                }
                trNode.innerHTML = "<td>"+record.usr + "</td><td>" + record.book 
                                    +"</td><td>" + convert(record.bt) 
                                    + "</td><td>" + returned + "</td>"
            }
        })
    })
}

var bindEvents = function () {
    bindEventShowClick()
}


var __main = function () {
    bindEvents()
}

__main()