# Generated by Django 4.1.7 on 2023-03-23 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0010_alter_datamodel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datamodel',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
