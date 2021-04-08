function News() {

};

//定义一个初始化ueditor
News.prototype.initUeditorEvent = function(){
    window.ue = UE.getEditor('editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'

    }) //把获取到的那个绑定到window上，用作全局变量。
}


News.prototype.listenUploadFilesEvent = function(){
    //获取上传的按钮
    var uploadBtn = $('#thumbnail-btn');
    //绑定上传的事件,这个事件是change(),不是之前的那个click事件了,这里要注意
    uploadBtn.change(function(){
        //因为当我们获取某一个标签的时候,其实获取到的是某一类的标签的集合,所以需要用下标来选择,
        //同时因为这里点击上传按钮的时候,浏览器可以选择多个文件,这就导致了,这个上传的文件也不是一个文件
        //而是一个文件的集合,是多个文件,所以还是需要用下标来标注获取到的文件,因为这里就是一个缩略图,所以是第零个

        //获取具体的一个文件,存放在第一个获取到的标签里面的第一个files里面.
        var file = uploadBtn[0].files[0];
        //需要把文件存放到FormData()对象中去,因为文件不能直接发送,先new一个对象,然后在调用对象的append方法
        var formData = new FormData();
        formData.append('file', file) //注意这个里面的参数第一个'file'是和view函数里面接收的是一样的.

        //封装file完成之后,调用Ajax超后台发送
        m_ajax.post({
            'url': '/cms/upload_files/',
            'data':formData, //这里直接传递我们上面封装好的formData就可以了,因为那个需要上传的文件就在formData中
            //下面两个需要传递的参数,一定要写,不屑不成功
            'processData': false,
            'contentType': false,

            'success': function(result){
                if(result['code']===200){
                    window.messageBox.showSuccess('上传图片成功！')
                    url = result['data']['url']
                    console.log(url)
                    var url_btn = $('#thumbnail')
                    url_btn.val(url)
                }
            }
        })
    });
}


News.prototype.run = function(){
    var self = this;
    self.listenUploadFilesEvent();
    self.initUeditorEvent();
};

$(function(){
    var news = new News();
    news.run();
})