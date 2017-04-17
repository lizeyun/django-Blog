#coding:utf-8
# @Time    : 17-3-16 下午3.16
# @Author  : lzz
# @Site    : blog
# @File    : views.py
# @Software: PyCharm

import re
import os
import json
import logging
import traceback
import datetime

from forms import CommentForm, AuthorForm
from django.shortcuts import render
from django.core.cache import caches
from models import Article, Tag, Comment
from django.db.models import Q
from django import template
from django.contrib import auth
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView, DetailView, TemplateView

# Create your views here.
#缓存
cache = caches['default']


class BaseMixin(object):
#获取上下文
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            #标签
            context['r_tag_list'] = Tag.objects.all()
          #  print context['r_tag_list']
            #文章列表按月份分类
            articles = Article.objects.all()
            year_month = set()
            for a in articles:
                # 例：year_month = ((2016,5),(2017,3))
                year_month.add((a.create_time.year, a.create_time.month)) # 以元组作为key，初始化字典
            counter = {}.fromkeys(year_month, 0)
            for a in articles:
                # 例：counter = {(2017,3):2, (2016,5):3}
                counter[(a.create_time.year, a.create_time.month)] += 1
            year_month_number = []
            for key in counter:
                 #例：[{'year':2017, 'month':3, 'counter':2}]
                year_month_number.append({"year": key[0], 'month': key[1], 'counter': counter[key]})
            year_month_number.sort(reverse = True) #sort
            context['year_month_number'] = year_month_number

            #读取用户ip addr
            if self.request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip = self.request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = self.request.META['REMOTE_ADDR']
            context['ip_address'] = ip

            #获取访问前十文章列表
            context['article_rank'] = \
                Article.objects.order_by("-click_count")[0:10]

            print 'self cur user is %s'%self.request.user

        except:
            print traceback.format_exc()

        return context

@csrf_exempt
def likefunc(request, id= ''):
    if request.is_ajax():
        print 'like ajax req'
        queryset = Article.objects.filter(id = id)
        article = queryset.get(id = id)
        print article.click_count
        article.like_count += 1
        article.save()
        print 'num is %s'%article.like_count
        return HttpResponse(json.dumps({'num': article.like_count}))
    else:
        raise Http404

class IndexView(BaseMixin, ListView):
    template_name = "index2.html"
    context_object_name = 'obj_list'

    def get_context_data(self, **kwargs):
        cache.delete('path')
        kwargs['tags'] = Tag.objects.all()
    #    kwargs['first_title'] = '首页'
        return super(IndexView, self).get_context_data(**kwargs)
    #返回所有状态正常的文章
    def get_queryset(self):
        obj_list = Article.objects.filter(status = 0)
        return obj_list

#获取文章详情
class ArticleView(BaseMixin, DetailView):
    queryset = Article.objects.filter(status=0)
    template_name = 'blog1.html'
    context_object_name = 'article_list'
    #主键值
    slug_field = 'pk'
    def get(self, request, *args, **kwargs):
        #统计文章访问次数
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        self.cur_user_ip = ip
        print '%s access your web' %self.cur_user_ip
        en_id = self.kwargs.get('pk')
        #取出缓存中ID=xx的文章访问历史记录IP

        #if not cache.get(en_id, []):
        #    cache.set(en_id, self.cur_user_ip, 50)

        visited_ips = cache.get(en_id, [])
        print ' %s The cache pool are %s' %(en_id, visited_ips)
        if self.cur_user_ip not in visited_ips:
            try:
                #尝试查找ID=xx是否存在
                article = self.queryset.get(id = en_id)
            except Article.DoesNotExist:
                print 'Aricle  not exist'
                raise Http404
            else:
                #新增一次访问记录
                article.click_count += 1
                article.save()
                visited_ips.append(self.cur_user_ip)
            cache.set(en_id, visited_ips, 30*60)
        return super(ArticleView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        path = cache.get('path', '')
        #导航
        kwargs['first_title'] = path
        kwargs["sec_title"] = '正文'
        #获取文章评论
        en_id = self.kwargs.get('pk', '')
        try:
            article = Article.objects.get(id = en_id)
            comments = Comment.objects.filter(article = article)
            kwargs['comments'] = comments
        except:
            pass
        return super(ArticleView, self).get_context_data(**kwargs)

#Search
class SearchView(BaseMixin, ListView):
    template_name = 'index2.html'
    context_object_name = 'obj_list'

    def get_context_data(self, *args, **kwargs):
        kwargs['first_title'] = '查找'
        kwargs['sec_title'] = self.request.GET.get('word', '')
        return super(SearchView, self).get_context_data(**kwargs)

    def get_queryset(self):
        word = self.request.GET.get('word', '')
        print 'search is %s'%word
        obj_list = Article.objects.filter(
            Q(title__icontains=word) |Q(content__icontains=word), status=0
        )
        return obj_list


#按时间归类
class DateArticleView(BaseMixin, ListView):
    template_name = 'index2.html'
    context_object_name = 'obj_list'
    #返回上下文的内容，
    def get_context_data(self, **kwargs):
        en_year = self.kwargs.get("year", "")
        en_month = self.kwargs.get("month", "")
        _date = en_year + '-' + en_month
        cache.set('path', _date)
        #这里是指路径栏
        kwargs["first_title"] = "时间分类"
        kwargs["sec_title"] = _date
        kwargs['tags'] = Tag.objects.all()
        return super(DateArticleView, self).get_context_data(**kwargs)
    #返回查看的x年x月的文章
    def get_queryset(self):
        en_year=self.kwargs.get("year", "")
        en_month=self.kwargs.get("month", "")
        print en_year, en_month
        if int(en_month)<10:
            strmonth="0"+en_month
        else:
            strmonth=en_month
        obj_list = Article.objects.filter(create_time__icontains= en_year+'-'+strmonth)
        return obj_list

#按标签分类
class TagView(BaseMixin, ListView):
    template_name = 'index2.html'
    context_object_name = 'obj_list'

    def get_context_data(self, **kwargs):
        en_tag = self.kwargs.get('tag_name', '')
        cache.set('path', en_tag)
        kwargs["first_title"] = "标签分类"
        kwargs["sec_title"] = en_tag
        kwargs['tags'] = Tag.objects.all()
        return super(TagView, self).get_context_data(**kwargs)

    def get_queryset(self):
        en_tag = self.kwargs.get("tag_name", '')
        try:
            tags = Tag.objects.get(name = en_tag)
            obj_list = Article.objects.filter(tags = tags)
            print 'tag is %s'%obj_list
        except Tag.DoesNotExist:
            obj_list = ''
            pass
        return obj_list


class PostCommentView(View):
    def post(self, request, *args, **kwargs):
    #if request.is_ajax(): #后面添加的，判断是否ajax请求
        print '''正在访问我啊 嘻嘻'''
        ar_id = self.kwargs.get('slug', '')
        try:
            article = Article.objects.get(id = ar_id)
        except Article.DoesNotExist:
            article = None
        print request.POST
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print 'com is %s'%cd
           # Comment.objects.create(cd)
            p = Comment( username = cd['username'],
                         email = cd['email'],
                         content = cd['content'],
                         article = article)
            p.save()
        else:
            cd = []
            print form.errors
        return HttpResponseRedirect('/blog/article/%s' %ar_id)
       # return HttpResponse(json.dumps({"content": cd['content']}))

#函数实现无刷新回复评论
@csrf_exempt
def postcomment(request, slug):

    if request.is_ajax():
        print 'cur is ajax req post'
        content = request.POST.get('content', '')
        ar_id = slug
        try:
            article = Article.objects.get(id=ar_id)
        except Article.DoesNotExist:
            article = None
        print request.POST
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Comment.objects.create(cd)
            p = Comment(username=cd['username'],
                        email=cd['email'],
                        content=cd['content'],
                        article=article)
            p.save()
            print 'save %s ok'%cd
        else:
            cd = []
            print form.errors
        content = {'username': cd['username'],
                   'content': cd['content'],
                   'create_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') }
        return HttpResponse(json.dumps({'content': content}))


class AuthorView(View):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        #获取是登录or注册
        slug = self.kwargs.get('slug', '')
        print 'action %s'%slug
        if slug == 'login':
            return self.login(request)
        if slug == 'regi':
            return self.regi(request)
        if slug == 'logout':
            return self.logout(request)

    def get(self, request, *args, **kwargs):

        # 如果是get请求直接返回404页面
        raise Http404

    def login(self, request):
        print 'you are login111111111'
        username = request.POST.get("username", '')
        passwd = request.POST.get("passwd", "")

        print 'renzheng %s' %username
        user = auth.authenticate(username= username, password= passwd)
        errors = []

        if user is not None:
            auth.login(request, user)
        else:
            errors.append('Account or passwd is not correct')

        mydict = {"errors": errors}
        return HttpResponse(json.dumps(mydict), content_type="application/json")

    def regi(self, request):
        username = request.POST.get("username", "")
        passwd = request.POST.get("passwd", "")
        re_passwd = request.POST.get("re_passwd", "")
        email = request.POST.get("email", "")
        print 'it is %s%s%s'%(username, passwd, email)
        form = AuthorForm(request.POST)
        errors = []
        print 'form dont konw valid'
        try:
            if form.is_valid():
                form.save()
                user = auth.authenticate(username= username, password= re_passwd)
                auth.login(request, user)
             #   errors.append('成功注册并已登录')
            else:
                print form.errors.items()
                for k, v in form.errors.items():
                    print k, v
                    # v.as_text() 详见django.forms.util.ErrorList 中
                    errors.append(v.as_text())

        except:
            print traceback.format_exc()
        #     #保存错误到列表


        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def logout(self, request):
        if not request.user.is_authenticated():
            print '未登录'
            raise Http404
        else:
            auth.logout(request)
            return HttpResponse('成功退出')



