# Generated by Django 4.1.7 on 2023-12-22 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_team_cover_photo_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='cover_photo_url',
            field=models.URLField(blank=True, default=None, max_length=250, null=True),
        ),
    ]
