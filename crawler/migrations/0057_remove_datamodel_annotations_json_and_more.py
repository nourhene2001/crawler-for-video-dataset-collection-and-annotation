# Generated by Django 4.1.7 on 2023-04-23 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0056_datamodel_annotations_json_datasetmodel_annotation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datamodel',
            name='annotations_json',
        ),
        migrations.RemoveField(
            model_name='datasetmodel',
            name='annotation',
        ),
        migrations.AddField(
            model_name='datamodel',
            name='annotation',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='datasetmodel',
            name='annotations_json',
            field=models.JSONField(blank=True, null=True),
        ),
    ]