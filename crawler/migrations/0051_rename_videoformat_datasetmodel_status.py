# Generated by Django 4.1.7 on 2023-04-08 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0050_datasetmodel_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datasetmodel',
            old_name='videoformat',
            new_name='status',
        ),
    ]
