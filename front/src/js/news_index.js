function NewsIndex() {
    var self = this;
    self.page = 2;
    self.category_id = 0;
    self.loadMoreBtn = $('#load_more_news')
}

NewsIndex.prototype.run = function () {
    var self = this;
    self.listenSwitchCategory();
    self.listenLoadMoreNews();
}

//点击左侧菜单板块category，进行切换
NewsIndex.prototype.listenSwitchCategory = function () {
    var self = this;
    var categoryGroup = $('.list-group-category')
    categoryGroup.children().click(function (event) {
        var li = $(this)
        var category_id = li.attr('data-id')
        var page = 1

        event.preventDefault();
        //向后端发送请求
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'p': page,
                'category_id': category_id
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var newses = result['data']
                    console.log(newses)
                    var tpl = template('test', {'newses': newses})
                    var news_item = $('.news_item')

                    news_item.empty()
                    news_item.append(tpl);

                    // 切换之后，要把page和category_id设置成下一次点击时候的条件
                    // 这个时候就可以看出把page 和category_id设置成全局变量的意义了，方便修改。
                    self.page = 2;
                    self.category_id = category_id;
                    self.loadMoreBtn.show();
                }
            }
        })

    })
}

// 点击加载更多美女资讯
NewsIndex.prototype.listenLoadMoreNews = function () {
    var self = this;
    var loadMoreBtn = $("#load_more_news");
    console.log(loadMoreBtn)
    loadMoreBtn.click(function (event) {
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'p': self.page,
                'category_id': self.category_id
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var newses = result['data']
                    console.log(newses)
                    if (newses.length > 0) {
                        var tpl = template('test', {'newses': newses})
                        var news_item = $(".news_item")
                        news_item.append(tpl);
                        //点击一次之后，要设置page加一，然后方便下一次点击的时候传递给后端函数。
                        self.page += 1;
                    } else {
                        loadMoreBtn.hide()
                    }
                }
            }
        })

    })
}


$(function () {
    var news_index = new NewsIndex();
    news_index.run()
})