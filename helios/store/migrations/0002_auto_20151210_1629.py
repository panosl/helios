# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='taxes',
            field=models.ManyToManyField(to='store.Tax', verbose_name='taxes', blank=True),
        ),
    ]
