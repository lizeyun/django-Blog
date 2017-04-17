# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_article_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(default=0, verbose_name=b'\xe4\xbd\x9c\xe8\x80\x85', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(default=b'/static/images/44.png', upload_to=b'article', null=True, verbose_name=b'\xe5\x9b\xbe\xe7\x89\x87\xe7\xae\x80\xe4\xbb\x8b', blank=True),
        ),
    ]
