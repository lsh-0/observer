# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-22 05:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observer', '0011_articlejson_ajson_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='num_citations_crossref',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='num_citations_pubmed',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='num_citations_scopus',
            field=models.PositiveIntegerField(default=0),
        ),
    ]