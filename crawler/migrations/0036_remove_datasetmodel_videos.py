# Generated by Django 4.1.7 on 2023-03-29 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0035_rename_video_video_dataset_videos_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasetmodel',
            name='videos',
        ),
    ]
