# Generated by Django 3.2.13 on 2022-12-05 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='explicit',
            field=models.BooleanField(default=False),
        ),
    ]
