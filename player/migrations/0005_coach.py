# Generated by Django 4.1.7 on 2023-12-20 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
        ('player', '0004_alter_player_major'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(default=None, max_length=100)),
                ('last_name', models.CharField(default=None, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('gender', models.CharField(choices=[('M', 'Men'), ('W', 'Women')], default=None, max_length=1)),
                ('team', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='coaches', to='team.team')),
            ],
        ),
    ]
