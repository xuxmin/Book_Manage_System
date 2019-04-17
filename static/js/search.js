
// 给train按钮绑定事件
var bindEventPointTrain = function(){
    var btn = e('#train')
    btn.addEventListener('click', function(event){
        var iter = e('#iter').value
        var perp = e('#perp').value
        var pca = e('#pca').value
        var lr = e('#lr').value
    
        var form ={
            iter: iter,
            perp: perp,
            pca: pca,
            lr: lr,
        }
        // 给服务器发送请求
        apiTrain(form,function(r){
            // 清除原来的svg子节点
            clearPoint()
            // 将返回的 json 数据解析，并添加svg
            var points = JSON.parse(r)
            
            // 归一化数据
            var max = 0
            for (var i = 0; i < points.length; i++){
                var point = points[i]
                if (point.x > max)
                    max = point.x
            }

            for (var i = 0; i < points.length; i++){
                var point = points[i]
                point.x = point.x / max
                point.y = point.y / max
                insertPoint(point)
            }
        })
        elem = e('svg')
        // 更新 svgPan
        svgPan = SVGPan(elem)
    })

}

var bindEventPointMouseOut = function() {
    var pointList = e('#group1')
    pointList.addEventListener('mouseout', function(event){
        var self = event.target
        log('event.target',self)
        self.setAttribute("stroke", "black");
    })
}


var bindEvents = function() {
    bindEventPointTrain()
    bindEventPointClick()
    bindEventPointMouseOver()
    bindEventPointMouseOut()
}


var __main = function() {
    bindEvents()
}

__main()
