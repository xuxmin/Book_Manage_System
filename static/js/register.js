var bindEventButtonClick = function () {
    var bt = document.querySelector("#id-register")

    bt.addEventListener('click', function (event) {
        var user = document.querySelector("#id-user")
        var pwd = document.querySelector("#id-pwd")
        console.log('ssssss:', user.value)
        console.log('sssss:', pwd.value)
        form = {}
        form['username'] = user.value
        form['password'] = pwd.value
        console.log('click')

        apiRegister(form, function (status, r) {
            if (status == 500) {
                alert("注册失败")
                return
            }
            o = JSON.parse(r)
            if (o['username'] == user.value) {
                alert("注册成功，正在跳转")
                window.location.assign("/")
            } else {
                alert("注册失败")
            }
        })


    })
}


var bindEvents = function () {
    bindEventButtonClick()
}


var __main = function () {
    bindEvents()
}

__main()