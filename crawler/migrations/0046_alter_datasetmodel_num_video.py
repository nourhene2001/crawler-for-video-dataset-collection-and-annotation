# Generated by Django 4.1.7 on 2023-03-31 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0045_datasetmodel_description_datasetmodel_max_v_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetmodel',
            name='num_video',
            field=models.IntegerField(default=0),
        ),
    ]