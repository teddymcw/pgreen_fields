# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings
import django.contrib.postgres.fields.hstore
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS hstore"),

        migrations.CreateModel(

            name='SolarPanel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('square_feet_access', django.contrib.postgres.fields.ranges.IntegerRangeField()),
                ('avail_team_period', django.contrib.postgres.fields.ranges.DateRangeField()),
                ('types_of_surface', django.contrib.postgres.fields.ArrayField(size=None, null=True, base_field=models.CharField(max_length=100, blank=True), blank=True)),
                ('unique_install_parameters', django.contrib.postgres.fields.hstore.HStoreField()),
                ('user', models.OneToOneField(related_name='account', verbose_name=b'user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
