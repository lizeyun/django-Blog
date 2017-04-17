# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170325_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(default=b'/static/images/44.png', upload_to=b'./article/images/', null=True, verbose_name=b'\xe5\x9b\xbe\xe7\x89\x87\xe7\xae\x80\xe4\xbb\x8b', blank=True),
        ),
    ]
