# Generated by Django 4.1.7 on 2023-12-20 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixture', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
