# Generated by Django 2.1.2 on 2020-08-10 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiktok_app', '0004_auto_20200809_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='bio',
            field=models.CharField(default='bio', max_length=200),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='instagram',
            field=models.CharField(default='instagram', max_length=200),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='youtube',
            field=models.CharField(default='youtube', max_length=200),
        ),
    ]
