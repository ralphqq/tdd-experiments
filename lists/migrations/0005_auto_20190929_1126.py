# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-29 03:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_item_parent_list'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('id',)},
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('parent_list', 'text')]),
        ),
    ]
