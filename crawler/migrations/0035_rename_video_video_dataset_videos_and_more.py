# Generated by Django 4.1.7 on 2023-03-29 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0034_video_dataset_alter_datasetmodel_videos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video_dataset',
            old_name='video',
            new_name='videos',
        ),
        migrations.AlterField(
            model_name='datasetmodel',
            name='videos',
            field=models.ManyToManyField(blank=True, through='crawler.video_dataset', to='crawler.datamodel'),
        ),
    ]
