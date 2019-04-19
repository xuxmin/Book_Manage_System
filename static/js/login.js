var bindEventButtonClick = function () {
    var bt = document.querySelector("#id-login")

    bt.addEventListener('click', function (event) {
        var user = document.querySelector("#id-user")
        var pwd = document.querySelector("#id-pwd")
        console.log('ssssss:', user.value)
        console.log('sssss:', pwd.value)
        form = {}
        form['username'] = user.value
        form['password'] = pwd.value
        console.log('click')

        apiLogin(form, function (status, r) {
            if (status == 500){
                alert("用户名或密码不正确")
                return 
            }
            o = JSON.parse(r)
            if (o['username'] == user.value) {
                alert("登陆成功，正在跳转")
                window.location.assign("/")
            } else {
                alert("登陆失败")
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