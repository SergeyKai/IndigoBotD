# Generated by Django 5.0.4 on 2024-04-07 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('hash_password', models.CharField(max_length=255)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('phone_number', models.CharField(max_length=255, null=True)),
                ('tg_id', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('date', models.DateField(null=True)),
                ('time', models.TimeField(null=True)),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='bot.direction')),
            ],
        ),
        migrations.CreateModel(
            name='SessionRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_records', to='bot.session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_records', to='bot.user')),
            ],
        ),
    ]
