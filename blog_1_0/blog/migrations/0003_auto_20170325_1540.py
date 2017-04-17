# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=50, null=True, verbose_name=b'\xe9\x82\xae\xe4\xbb\xb6\xe5\x9c\xb0\xe5\x9d\x80', blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.IntegerField(default=0, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, '\u6b63\u5e38'), (1, '\u8349\u7a3f'), (2, '\u5220\u9664')]),
        ),
    ]
