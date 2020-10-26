function BeautyTags(){}

BeautyTags.prototype.run = function(){
    var self = this;
    self.listenAddTagsEvent();
    self.listenEditTagsEvent();
    self.listenDelTagsEvent();

}

//定义监听增加标签的事件
BeautyTags.prototype.listenAddTagsEvent = function(){
    //获取新增的按钮
    var addBtn = $('#add-btn')
    //绑定点击事件
    addBtn.click(function () {
        //弹框出来一个添加的功能
        xfzalert.alertOneInput({
           'title': '请输入要添加的美女标签',
           'placeholder': '美女标签',
           'confirmCallback':function(inputValue){
              xfzajax.post({
                 'url':'/cms/write_beauty_tag/',
                 'data': {
                     'tag': inputValue
                 },
                 'success': function(result){
                     if(result['code']===200){
                         window.location.reload()
                     }else {
                         xfzalert.close()
                     }
               }
              })
        }
        })
    })
}

//定义监听修改标签的事件
BeautyTags.prototype.listenEditTagsEvent = function(){
    //获取点击修改的按钮
    var editBtn = $('.edit_tag_btn')
    //绑定点击事件
    editBtn.click(function(){
        var self = $(this)
        //获取点击同时的值
        var tr = self.parent().parent()
        var pk = tr.attr('data-pk')
        var tag = tr.attr('data-tag')

        //弹出框
        xfzalert.alertOneInput({
           'title': '请输入需要修改的值',
           'value': tag,
           'confirmCallback':function(inputValue){
               if(inputValue===tag){
                   xfzalert.alertErrorToast('跟原来的值一样,不修改乱点什么!')

               }else{
                   xfzajax.post({
                  'url': '/cms/edit_beauty_tag/',
                  'data':{
                      'pk':pk,
                      'tag':inputValue
                  },
                  'success':function(result){
                      if(result['code']===200){
                          //如果成功,关闭这个框框
                      window.location.reload()
                      }
                  }
              })
               }
           }
        })
    })

}


//定义监听删除标签的事件
BeautyTags.prototype.listenDelTagsEvent = function(){
    //获取删除的按钮
    var delBtn = $('.delete_tag_btn')
    //绑定点击事件
    delBtn.click(function(){
        //只需要吧想要删除的标签的id传递给视图函数就可以
        var self = $(this)
        var tr = self.parent().parent()
        var pk = tr.attr('data-pk')
        xfzajax.post({
            'url':'/cms/delete_beauty_tag/',
            'data':{
                'pk':pk
            },
            'success':function (result) {
               if(result['code']===200){
                   xfzalert.alertSuccessToast('删除标签成功')
                   window.location.reload()
               }
            }
            
            
        })
    })
}


$(function () {
    var beauty_tags = new BeautyTags();
    beauty_tags.run();
})