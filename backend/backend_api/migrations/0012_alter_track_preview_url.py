# Generated by Django 3.2.13 on 2022-11-01 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0011_auto_20221101_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='preview_url',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]