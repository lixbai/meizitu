$(function() {
    // $('.father').mouseover(function(){
    // 	console.log('father被移入了')
    // })
    // $('.father').mouseout(function(){
    // 	console.log('father被移出了.')
    // })

    // 换另外一个方式: mouseenter / mouseleave
    // $('.father').mouseenter(function(){
    // 	console.log('father被移入了')
    // })
    // $('.father').mouseleave(function(){
    // 	console.log('father被移出了.')
    // })

    //hover 2个参数
    // $('.father').hover(function(){
    // 	console.log('father 被移入了')
    // }, function(){
    // 	console.log('father 被移出了.')
    // })

    //Hover 一个参数
    $("svg").hover(function() {

        //获取被点击的i标签的索引号
        var m = $(this).index("svg");

        for (var i = 0; i < 5; i++) {
            //把索引号及之前的星星变色
            if (i <= m) {
                $("svg:eq(" + i + ")").attr("fill", "#ffc107");
            } else { //后面的就变空
                $("svg:eq(" + i + ")").attr("fill", "#6c757d");
            }

        }
    })

})