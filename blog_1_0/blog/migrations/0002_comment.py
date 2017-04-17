# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe5\x86\x85\xe5\xae\xb9')),
                ('username', models.CharField(max_length=30, verbose_name=b'\xe6\x98\xb5\xe7\xa7\xb0')),
                ('email', models.EmailField(max_length=50, null=True, verbose_name=b'\xe8\x81\x94\xe7\xb3\xbb\xe5\x9c\xb0\xe5\x9d\x80', blank=True)),
                ('status', models.ImageField(default=0, upload_to=b'', verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, '\u6b63\u5e38'), (1, '\u8349\u7a3f'), (2, '\u5220\u9664')])),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('article', models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe6\x96\x87\xe7\xab\xa0', to='blog.Article')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name_plural': '\u8bc4\u8bba\u7ba1\u7406',
            },
        ),
    ]
