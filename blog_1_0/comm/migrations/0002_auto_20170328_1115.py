# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replay',
            name='replay_time',
        ),
        migrations.AlterField(
            model_name='replay',
            name='replay_user',
            field=models.CharField(default=b'admin', max_length=20, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe7\x94\xa8\xe6\x88\xb7', blank=True),
        ),
    ]
