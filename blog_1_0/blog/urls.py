# -*- coding: utf-8 -*-
# @Time    : 17-3-17 下午12:18
# @Author  : lzz
# @Site    : blog
# @File    : urls.py
# @Software: PyCharm

#url路由

from django.conf.urls import url
#from django.contrib import admin
from views import IndexView, TagView, DateArticleView, ArticleView, likefunc, PostCommentView, SearchView, postcomment
from views import AuthorView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'tag/(?P<tag_name>.+)/$', TagView.as_view(), name='tag_view'),
    url(r'^article/(?P<pk>.+)/$', ArticleView.as_view(), name='article_view'),
    url(r'^search$', SearchView.as_view(), name='search_view'),
    url(r'^like/(?P<id>.+)/$', likefunc, name='like_view'),
    url(r'^user/(?P<slug>\w+)/$', AuthorView.as_view(), name='auth_view'),
  #  url(r'^comment/(?P<slug>\w+)/$', PostCommentView.as_view(), name='postcomment-view'),
    url(r'^comment/(?P<slug>\w+)/$', postcomment),
    #url(r"^flush_comment/(?P<slug>\w+)/$", flush_comment),
    url(r'^datearticle/(?P<year>\d+)/(?P<month>\d+)/$', DateArticleView.as_view(), name='datearticle_view')

]