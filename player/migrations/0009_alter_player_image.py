# Generated by Django 4.1.7 on 2023-12-22 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0008_alter_player_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='image',
            field=models.URLField(default=None, max_length=250),
        ),
    ]
