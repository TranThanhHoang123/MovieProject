# Generated by Django 5.0.6 on 2024-07-02 08:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmapp', '0010_alter_moviegenre_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieEpisode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episode_number', models.PositiveIntegerField()),
                ('video_file', models.FileField(default='Film/Default.mp4', upload_to='Film/%Y/%m')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='filmapp.movie')),
            ],
            options={
                'unique_together': {('movie', 'episode_number')},
            },
        ),
    ]