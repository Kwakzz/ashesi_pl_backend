# Generated by Django 4.1.7 on 2023-12-20 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=50, unique=True)),
                ('name_abbreviation', models.CharField(default=None, max_length=5, unique=True)),
                ('logo_url', models.URLField(default=None)),
                ('color', models.CharField(default=None, max_length=20)),
                ('twitter_url', models.URLField(default=None, max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
