# Generated by Django 4.1.7 on 2023-03-29 21:10

import django
from django.db import migrations, models

def migrate_data(apps, schema_editor):
    VideoInDataset = apps.get_model('crawler', 'VideoInDataset')
    for dataset in apps.get_model('crawler', 'datasetModel').objects.all():
        for video in dataset.videos.all():
            VideoInDataset.objects.create(video=video, dataset=dataset)
class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0040_auto_20230329_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoInDataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawler.datasetModel')),
                ('videos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawler.dataModel')),
            ],
        ),
        migrations.RunPython(migrate_data),
        migrations.RemoveField(
            model_name='datasetModel',
            name='videos',
        ),
        migrations.AddField(
            model_name='datasetModel',
            name='videos',
            field=models.ManyToManyField(blank=True, to='crawler.dataModel', through='crawler.VideoInDataset'),
        ),
    ]
