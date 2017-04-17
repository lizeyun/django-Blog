#coding:utf-8
from django.db import models

class Post(models.Model):
    username = models.CharField(max_length=20, verbose_name='post user')
    content = models.TextField()

    def __unicode__(self):
        return self.username

# Create your models here.
class Replay(models.Model):
    replay_content = models.TextField()
    post = models.ForeignKey(Post)
 #   replay_time = models.DateTimeField(verbose_name='回复时间', editable= )

    replay_user = models.CharField(max_length= 20, verbose_name= '评论用户',blank= True, default= 'admin')

    def __unicode__(self):
        return self.replay_content