# Generated by Django 5.1.1 on 2024-09-11 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('civitapp', '0002_topic_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
