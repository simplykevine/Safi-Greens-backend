# Generated by Django 5.2.4 on 2025-07-20 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('is_mama_mboga', models.BooleanField(default=False)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
