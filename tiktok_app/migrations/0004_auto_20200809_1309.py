# Generated by Django 2.1.2 on 2020-08-09 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiktok_app', '0003_auto_20200809_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testvideofile',
            name='audiofile',
        ),
        migrations.RemoveField(
            model_name='testvideofile',
            name='user',
        ),
        migrations.AlterField(
            model_name='videofile',
            name='video_file',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.DeleteModel(
            name='TestVideoFile',
        ),
    ]
