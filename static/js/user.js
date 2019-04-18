var bindEventPointClick = function () {
    // 所以我们先找到 book-list, 给其绑定click 事件
    var bookList = e('#book-list')
    bookList.addEventListener('click', function (event) {
        // 我们可以通过 event.target 来得到被点击的元素
        var b = event.target
        log('event.target', b)
        if (b.className != 'return')
            return
        // 获取该节点的父节点
        var book = b.parentNode.parentNode
        log('parentNode.parentNode:', book)

        var title = book.firstElementChild.textContent

        // 利用return book api 发送请求, 
        apiReturn(title, function (r) {
            log('r: ', r)
            var o = JSON.parse(r)
            log("o:", o)
            if (o.deleted == "0") {
                alert("归还失败")
            } else {
                alert("归还成功")
                b.textContent = "已归还"
                b.disabled = "disabled"
                var time = new Date().format("yyyy-MM-dd hh:mm:ss")
                book.lastElementChild.previousElementSibling.textContent = time
            }
        })
    })
}


var bindButton = function () {

    var bts = document.getElementsByClassName("return")
    for (var i = 0; i < bts.length; i++) {
        if (bts[i].value != 0) {
            bts[i].textContent = "已归还"
            bts[i].disabled = "disabled"
        } else {
            bts[i].textContent = "还书"
        }
    }

}

var bindEvents = function () {
    bindEventPointClick()
    bindButton()
}


var __main = function () {
    bindEvents()
}

__main()