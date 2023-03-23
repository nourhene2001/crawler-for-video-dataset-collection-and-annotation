# Generated by Django 4.1.7 on 2023-03-23 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0013_alter_datamodel_resolution_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datamodel',
            name='description',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='videoformat',
            field=models.CharField(choices=[('mp4', 'mp4'), ('WebM', 'WebM'), ('3GP', '3GP')], default='mp4', max_length=20),
        ),
    ]
