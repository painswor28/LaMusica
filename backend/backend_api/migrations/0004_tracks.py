# Generated by Django 3.2.13 on 2022-11-01 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0003_songs_tempo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracks',
            fields=[
                ('uri', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('id', models.CharField(max_length=25)),
                ('danceability', models.IntegerField()),
                ('energy', models.IntegerField()),
                ('loudness', models.IntegerField()),
                ('speechiness', models.IntegerField()),
                ('acousticness', models.IntegerField()),
                ('instrumental', models.IntegerField()),
                ('liveness', models.IntegerField()),
                ('valance', models.IntegerField()),
                ('tempo', models.IntegerField()),
                ('duration_ms', models.IntegerField()),
                ('time_signature', models.IntegerField()),
                ('camelot_key', models.IntegerField()),
                ('popularity', models.IntegerField()),
                ('explicit', models.BooleanField()),
                ('preview_url', models.CharField(max_length=100)),
                ('spotify_url', models.CharField(max_length=100)),
            ],
        ),
    ]