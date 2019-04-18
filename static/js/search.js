var bindEventPointClick = function () {
    // 所以我们先找到 book-list, 给其绑定click 事件
    var bookList = e('#book-list')
    var card = e('#id-card')
    var card_id = card.textContent

    if (card_id == "None"){
        alert("申请借书证后才能开始借书")
    }
        
    bookList.addEventListener('click', function (event) {
        if (card_id == "None") {
            alert("您没有借书证哦")
            return
        }
        // 我们可以通过 event.target 来得到被点击的元素
        var b = event.target
        log('event.target', b)

        if (b.className != 'borrow')
            return

        // 获取该节点的父节点
        var book = b.parentNode.parentNode
        log('parentNode.parentNode:', book)

        var title = book.firstElementChild.textContent
        var stock = book.lastElementChild.previousElementSibling

        // 利用borrow book api 发送请求, 
        apiBorrow(title, function (r) {
            log('r: ', r)
            var o = JSON.parse(r)
            log("o:", o)
            if (o.stock == "-1") {
                alert("借阅失败")
            } else {
                alert("借阅成功")
                b.textContent = "已借阅"
                stock.textContent = o.stock
                b.disabled = "disabled"
            }
        })
    })
}

var bindButton = function () {
    var form = ""
    apiBorrowedBook(form, function (r) {
        log('r: ', r)
        var o = JSON.parse(r)
        log("o:", o)
        var bts = document.getElementsByClassName("borrow")

        for (var i = 0; i < bts.length; i++) {
            title = bts[i].parentElement.parentElement.firstElementChild
            if (o.indexOf(title.textContent) > -1) {
                bts[i].textContent = "已借阅"
                bts[i].disabled = "disabled"
            } 
        }
    })


}


var bindEvents = function () {
    bindEventPointClick()
    bindButton()
}


var __main = function () {
    bindEvents()
}

__main()