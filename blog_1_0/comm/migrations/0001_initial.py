# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=20, verbose_name=b'post user')),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Replay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('replay_content', models.TextField()),
                ('replay_time', models.DateTimeField(default=b'admin', verbose_name=b'\xe5\x9b\x9e\xe5\xa4\x8d\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('replay_user', models.CharField(max_length=20, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe7\x94\xa8\xe6\x88\xb7')),
                ('post', models.ForeignKey(to='comm.Post')),
            ],
        ),
    ]
