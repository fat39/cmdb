# Generated by Django 2.0.1 on 2018-03-05 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disk',
            name='capacity',
            field=models.CharField(max_length=32, verbose_name='磁盘容量GB'),
        ),
    ]
