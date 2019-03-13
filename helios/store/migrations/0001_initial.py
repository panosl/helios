# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('desc', models.TextField(verbose_name='description', blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('parent', models.ForeignKey(related_name='child_set', on_delete=models.SET_NULL, blank=True, to='store.Category', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name='name')),
                ('desc', models.TextField(verbose_name='description', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=80)),
                ('is_active', models.BooleanField(default=True, help_text='The collection will be available in the store.', verbose_name='active')),
            ],
            options={
                'verbose_name': 'collection',
                'verbose_name_plural': 'collections',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name='name')),
                ('slug', models.SlugField(unique=True, max_length=80)),
                ('desc', models.TextField(verbose_name='description', blank=True)),
                ('date_added', models.DateField(auto_now_add=True, verbose_name='date added')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('is_active', models.BooleanField(default=True, help_text='The product will appear in the store.', verbose_name='active')),
                ('base_price', models.DecimalField(verbose_name='base price', max_digits=6, decimal_places=2)),
                ('is_featured', models.BooleanField(default=False, help_text='The product will be featured on the front page.', verbose_name='featured')),
                ('stock', models.IntegerField(default=0, help_text='Number of items in stock.', verbose_name='stock')),
                ('weight', models.PositiveIntegerField(default=0, help_text='Defined in kilograms.', verbose_name='weight')),
                ('category', models.ForeignKey(verbose_name='category', on_delete=models.SET_NULL, blank=True, to='store.Category', null=True)),
            ],
            options={
                'ordering': ['-is_featured', '-last_modified'],
                'abstract': False,
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'./product_images', verbose_name='picture')),
                ('list_position', models.PositiveIntegerField(default=1, verbose_name='list position')),
                ('product', models.ForeignKey(verbose_name='product', on_delete=models.CASCADE, blank=True, to='store.Product', null=True)),
            ],
            options={
                'ordering': ['list_position'],
                'verbose_name': 'product image',
                'verbose_name_plural': 'product images',
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name='name')),
                ('desc', models.TextField(verbose_name='description', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=80)),
                ('rate', models.DecimalField(default=19.0, verbose_name='tax rate', max_digits=4, decimal_places=2)),
                ('is_active', models.BooleanField(default=True, help_text='The tax will be available in the store.', verbose_name='active')),
            ],
            options={
                'verbose_name': 'tax',
                'verbose_name_plural': 'taxes',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='taxes',
            field=models.ManyToManyField(to='store.Tax', null=True, verbose_name='taxes', blank=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='products',
            field=models.ManyToManyField(to='store.Product'),
        ),
    ]
