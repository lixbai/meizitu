function ManageNews() {
    window.tagArray = new Array();

}

/*
* 针对这里的操作，有一个限制问题，就是只能新增和删除，不能进行修改
* 新增--> 查询有，就直接显示。查询到没有，就add
* 删除--> 也只是在HTML 页面进行删除操作
* */

// 对标签 的增加标签
ManageNews.prototype.listenAddTag = function () {
    var self = this;
    var addTagBtn = $('.add_tag_btn')
    addTagBtn.click(function () {
        m_alert.alertOneInput({
            'title': '请输入要添加的文章标签',
            'placeholder': '文章标签',
            'confirmCallback': function (inputValue) {
                var cleanValue = $.trim(inputValue)
                // ajax存入数据库
                m_ajax.post({
                    'url': '/cms/news_add_tags/',
                    'data': {
                        'tag': cleanValue
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            //局部显示数据，并且刷新
                            var data = result['data']
                            console.log(data)
                            var pk = data['id']
                            var tagData = data['tag']
                            var code = data['code']
                            console.log(pk)
                            console.log(tagData)
                            console.log(code)
                            var add_cut_html = $('.add_cut_html')
                            var del_html = $('.del_html')
                            var ul = $('.tags-list')
                            if (code === 1) {
                                // 系统内没有，然后新添加
                                ul.append("<li class='badge badge-success'>" + "<span class='SpanBtn' data-id=" + pk + " code-id=" + code + ">" + tagData + "</span>" + add_cut_html.html() + "</li>")
                                // 同时把这个标签的ID，放到tagArray数组里面，这样留给后面的用
                                tagArray.push(pk)
                                console.log(tagArray)
                            } else {
                                // 系统内有，把系统内有的拿出来放到这个地方
                                ul.append("<li class='badge badge-warning'>" + "<span class='SpanBtn' data-id=" + pk + " code-id=" + code + ">" + tagData + "</span>" + del_html.html() + "</li>")
                                tagArray.push(pk)
                                console.log(tagArray)
                            }

                            m_alert.close()
                        }
                    }
                })
            }
        })
    })
}

// 对标签的 编辑操作
ManageNews.prototype.listenEditTag = function () {
    var self = this;

    // 这是要做时间委派，就是在这个标签还没有生成的时候，就把时间委派到父级元素上面去，要不然点击没反应
    $('.tagBtn').on('click', '.edit_tag_btn', function () {
        var self = $(this)
        var editSpanBtn = self.parent().prev()
        var oldTagData = $.trim(editSpanBtn.text())

        m_alert.alertOneInput({
            'title': '请输入新的标签',
            'value': oldTagData,
            'confirmCallback': function (inputValue) {
                var cleanInputValue = $.trim(inputValue)
                if (cleanInputValue === oldTagData) {
                    m_alert.alertErrorToast('跟原来的值一样,不修改乱点什么!')
                } else {
                    // 发送给数据库
                    m_ajax.post({
                        'url': '/cms/news_edit_tags/',
                        'data': {
                            'pk': editSpanBtn.attr('data-id'),
                            'tag': cleanInputValue
                        },
                        'success': function (result) {
                            if (result['code'] === 200) {
                                // 设置新值到相应给位置上面
                                var data = result['data']
                                var pk = data['id']
                                var tagData = data['tag']
                                var code = data['code']

                                editSpanBtn.attr('data-id', pk)
                                editSpanBtn.attr('code-id', code)
                                editSpanBtn.text(tagData)
                                m_alert.close()
                            } else {
                                m_alert.alertErrorToast(result['message'])
                            }
                        }
                    })
                    console.log(cleanInputValue)
                }
            }
        })
    })

}

// 点击删除li标签 对标签的删除操作
ManageNews.prototype.listenDelTag = function () {
    var self = this;
    // 做时间委派，委派到父级元素上面去，要不然无法点击
    $('.tagBtn').on('click', '.del_tag_btn', function () {
        var self = $(this)
        // 如果code=0，表示在数据库中已经存在的数据，直接拿出来用的。则不对数据库进行删除操作,只删除html页面
        // 如果code=1 表示新插入的数据，暂时还没有其他文章进行引用，则可以对数据库进行操作，同时删除HTML页面
        var SpanBtn = self.parent().prev()
        var delLiBtn = self.parent().parent()
        var pk = SpanBtn.attr('data-id')
        console.log(pk)
        if (SpanBtn.attr('code-id') === 1) {
            m_ajax.post({
                'url': '/cms/news_del_tags/',
                'data': {
                    'pk': pk
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        tagArray = $.grep(tagArray, function (value, index) {
                            return value != pk
                        })
                        console.log(tagArray)
                        delLiBtn.remove()
                    }
                }
            })
        } else {
            console.log(pk)
            tagArray = $.grep(tagArray, function (value, index) {
                return value != pk
            })
            console.log(tagArray)
            delLiBtn.remove()
        }
    })
}


ManageNews.prototype.listenSubmitNews = function () {
    var self = this;

    $('#submitBtn').click(function () {

        // 创建一个数组，把选中的option的值，存进去
        var categoryArray = []

        // 标题title
        var title = $('#title').val()
        // console.log(title)

        // 分类category， 数组形式
        $('#category option:selected').each(function () {
            var self = $(this)
            // 创建一个数组，把选中的option的值，存进去
            categoryArray.push(parseInt(self.val()))
        })
        // console.log(categoryArray)

        // 简介desc
        var desc = $('#desc').val()
        // console.log(desc)

        // 文章标签tag， 数组形式
        // console.log(tagArray)

        // 文章内容content
        // var content = $('#editor')
        // ue.ready(function() {
        //     //设置编辑器的内容
        //     // ue.setContent('hello');
        //     //获取html内容，返回: <p>hello</p>
        //     var html = ue.getContent();
        //     //获取纯文本内容，返回: hello
        //     var txt = ue.getContentTxt();
        //     // console.log(html)
        // });

        // 对tagArray数组元素去重
        var new_tagArray = [];
        for (var i = 0; i < tagArray.length; i++) {
            var items = tagArray[i];
            //判断元素是否存在于new_arr中，如果不存在则插入到new_ar中
            if ($.inArray(items, new_tagArray) === -1) {
                new_tagArray.push(items);
            }
        }


        // 缩略图 thumbnail
        var thumbnail = $('#thumbnail').val()
        console.log(thumbnail)


        // $('body').on('click', '#submitBtn',function () {
        // 用ajax 进行上传到后台
        m_ajax.post({
            'url': '/cms/ajax_news_post/',
            'data': {
                'title': title,
                'desc': desc,
                'thumbnail': thumbnail,
                'content': window.ue.getContent(),
                'category_array': JSON.stringify(categoryArray),
                'tag_array': JSON.stringify(new_tagArray),
                'dataType': 'json'
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    m_alert.alertSuccessToast('发布成功！',function () {
                        window.location.reload()
                    })
                }
            }
        })
    })


}


ManageNews.prototype.run = function () {
    var self = this;
    self.listenAddTag();
    self.listenEditTag();
    self.listenDelTag();
    self.listenSubmitNews();
}

$(function () {
    var manage_news = new ManageNews();
    manage_news.run();
})