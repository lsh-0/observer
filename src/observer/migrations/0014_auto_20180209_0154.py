# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-09 01:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observer', '0013_auto_20180202_0618'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('orcid', models.CharField(max_length=19)),
                ('datetime_record_created', models.DateTimeField(auto_now_add=True, help_text='added to the *observer database*, not date of profile creation')),
            ],
            options={
                'ordering': ('-datetime_record_created',),
            },
        ),
        migrations.AlterField(
            model_name='articlejson',
            name='ajson_type',
            field=models.CharField(choices=[('lax-ajson', 'lax article json'), ('elife-metrics-summary', 'elife-metrics summary data'), ('presspackage-id', 'presspackage summary data'), ('profile-id', 'profiles')], max_length=25),
        ),
    ]
