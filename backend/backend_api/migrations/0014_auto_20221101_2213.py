# Generated by Django 3.2.13 on 2022-11-01 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0013_alter_track_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.RemoveField(
            model_name='songs',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='songs',
            name='songKey',
        ),
        migrations.RemoveField(
            model_name='songs',
            name='tempo',
        ),
        migrations.AddField(
            model_name='songs',
            name='name',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='songs',
            name='songs',
            field=models.ManyToManyField(blank=True, related_name='songs', to='backend_api.Artist'),
        ),
    ]
