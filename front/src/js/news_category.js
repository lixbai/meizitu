function NewsCategory() {

}

NewsCategory.prototype.run = function(){
    var self = this;
    self.listenAddTagsBtnEvent();
    self.listenEditTagsEvent();
    self.listenDeleteTagsEvent();
};

//定义监听点击添加标签的事件
NewsCategory.prototype.listenAddTagsBtnEvent = function(){
    //获取点击标签
    var addbtn = $('#add-btn');
    //绑定点击事件
    addbtn.click(function(){
        m_alert.alertOneInput({
            'title': '请输入标签',
            'placeholder': '添加标签',
            'confirmCallback':function(inputValue){
                m_ajax.post({
                    'url': '/cms/write_news_category/',
                    'data': {
                        'category': $.trim(inputValue)
                    },
                    'success': function(result){
                        if(result['code']===200){
                            console.log(result)
                            window.location.reload()
                        }
                        else{
                            m_alert.close()
                        }
                    }
                })
            }
        });
    })

};

//定义监听编辑标签的按钮的事件
NewsCategory.prototype.listenEditTagsEvent = function(){
    var self = this;
    //获取编辑的按钮
    var editBtn = $('.edit_tag_btn');
    //绑定点击事件
    editBtn.click(function(){
        var self = $(this); //这个this是关键
        //拿到tr标签，因为上面绑定了主键和对应的数值
        var tr = self.parent().parent();
        var pk = tr.attr('data-pk');
        var tag = tr.attr('data-tag');
        console.log(tag)

        m_alert.alertOneInput({
            'title': '请填入新的标签名字',
            'value': tag,
            'confirmCallback': function (inputValue) {
                if(inputValue===tag){
                    m_alert.alertErrorToast('跟原来的值一样,不修改乱点什么!')
                }else {
                     m_ajax.post({
                  'url': '/cms/edit_news_category/',
                  'data': {
                      'pk': pk,
                      'category':inputValue,
                  },
                  'success': function(result){
                      if(result['code']===200){
                          console.log(name)
                          window.location.reload()
                      }
                  }
              })
                }


            }
        })
    })
};


NewsCategory.prototype.listenDeleteTagsEvent = function(){
    var del_tag_btn = $('.delete_tag_btn');
    del_tag_btn.click(function(){
        var self = $(this);
        var tr = self.parent().parent();
        var pk = tr.attr('data-pk');
        console.log(pk)
        m_ajax.post({
            'url':'/cms/del_news_category/',
            'data': {
                'pk': pk,
            },
            'success': function (result) {
                if(result['code']===200){
                   m_alert.alertConfirm({
                       'text':'确认删除吗',
                       'confirmCallback': function(){
                           window.location.reload()
                       }
                   })

                }
            }

        })
    })
}


$(function () {
    var news_category = new NewsCategory();
    news_category.run();
});
