# -*- coding: utf-8 -*-
# @Time    : 17-3-16 下午3.16
# @Author  : lzz
# @Site    : blog
# @File    : models.py
# @Software: PyCharm
import os
from django.db import models
from PIL import Image
from django.contrib.auth.models import User
# Create your models here.

# 文章等发布内容的状态
STATUS={
    0:u'正常',
    1:u'草稿',
    2:u'删除',
}


def make_pic(infile, outfile, width, height):
    """按照固定尺寸处理图片"""
    im = Image.open(infile)
    out = im.resize((width, height), Image.ANTIALIAS)
    out.save(outfile)

# class User(AbstractUser):
#     site_url = models.URLField(max_length=150, blank=True,
#                                null=True, verbose_name="个人链接")
#     class Meta:
#         verbose_name_plural = u'用户管理'
#         ordering = ['-id']
#
#     def __unicode__(self):
#         return self.username
#     __str__ = __unicode__

class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        verbose_name_plural = '标签管理'

    def __unicode__(self):
        return self.name
    __str__ = __unicode__

class Article(models.Model):
    title = models.CharField(max_length=40, verbose_name='文章标题')
    content = models.TextField(verbose_name='文章内容')
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    image = models.ImageField(verbose_name="图片简介", upload_to='article', blank=True, null=True,default="44.png")
    click_count = models.IntegerField(default=0, verbose_name='访问次数')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    status = models.IntegerField(default=0, choices=STATUS.items(), verbose_name='状态')

    class Meta:
        verbose_name = '文章管理'
        ordering = ['-create_time']

    def save(self, *args, **kwargs):
        print 'cur path is %s'%self.image.path
        print self.image.name
        small_path = './article/'
        base, ext = os.path.splitext(os.path.basename(self.image.path))
        super(Article, self).save(*args, **kwargs)
        #base yasuo .ext .jpg
        img_url = os.path.join(r'D:\desktop\django\blog_1_0\blog_1_0\media',self.image.name)
        make_pic(img_url,img_url, 500, 356)
       # self.image = os.path.join(small_path, self.image.name)
        #super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
    __str__ = __unicode__


class Comment(models.Model):
    content = models.TextField(verbose_name= '评论内容')
    username = models.CharField(max_length=30, verbose_name='昵称')
    # author = models.ForeignKey(User, verbose_name='作者')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮件地址')
    article = models.ForeignKey(Article, verbose_name='所属文章')
    status = models.IntegerField(default=0, choices=STATUS.items(), verbose_name='评论状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        verbose_name_plural = u'评论管理'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.content
    __str__ = __unicode__








