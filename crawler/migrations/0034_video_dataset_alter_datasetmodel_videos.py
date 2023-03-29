# Generated by Django 4.1.7 on 2023-03-29 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0033_datasetmodel_videos'),
    ]

    operations = [
        migrations.CreateModel(
            name='video_dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawler.datasetmodel')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawler.datamodel')),
            ],
        ),
        migrations.RemoveField(
            model_name='datasetmodel',
            name='videos',
        ),
        migrations.AddField(
            model_name='datasetmodel',
            name='videos',
            field=models.ManyToManyField(through='crawler.video_dataset', to='crawler.datamodel'),
        ),
        
    ]
