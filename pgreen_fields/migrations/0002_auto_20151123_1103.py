# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pgreen_fields', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solarpanel',
            name='user',
            field=models.OneToOneField(related_name='stub', verbose_name=b'user', to=settings.AUTH_USER_MODEL),
        ),
    ]
