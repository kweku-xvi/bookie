# Generated by Django 4.2.1 on 2024-06-17 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0004_event_short_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='short_description',
            field=models.CharField(max_length=200),
        ),
    ]
