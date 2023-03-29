# Generated by Django 4.1.7 on 2023-03-29 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0038_auto_20230329_2123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video_dataset',
            name='dataset',
        ),
        migrations.AddField(
             model_name='video_dataset',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_dataset', to='crawler.datasetmodel'),
        ),
        migrations.RemoveField(
            model_name='video_dataset',
            name='videos',
        ),
        migrations.AddField(
            model_name='video_dataset',
            name='videos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_dataset', to='crawler.datamodel'),
        ),
        
    ]
