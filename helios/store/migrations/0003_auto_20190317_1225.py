# Generated by Django 2.1.7 on 2019-03-17 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20151210_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='picture',
            field=models.ImageField(upload_to='./product_images', verbose_name='picture'),
        ),
    ]
