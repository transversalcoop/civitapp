# Generated by Django 5.1.1 on 2024-11-13 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('civitapp', '0003_answer_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content',
            field=models.JSONField(),
        ),
    ]
