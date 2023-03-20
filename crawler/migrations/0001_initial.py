# Generated by Django 4.1.7 on 2023-03-19 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=50)),
                ('video_format', models.CharField(choices=[('1', 'MP4'), ('2', 'AVI'), ('3', 'WebM'), ('3', '3GP'), ('3', 'FLV'), ('3', 'MKV')], max_length=50)),
                ('max_result', models.IntegerField()),
            ],
        ),
    ]
