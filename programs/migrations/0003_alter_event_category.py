# Generated by Django 4.2.1 on 2024-07-04 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0002_alter_event_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.CharField(choices=[('arts', 'Arts'), ('business', 'Business'), ('concert', 'Concert'), ('education', 'Education'), ('Fashion', 'Fashion'), ('Film', 'Film'), ('Food', 'Food'), ('Politics', 'Politics'), ('Health', 'Health'), ('Music', 'Music'), ('Science & Technology', 'Science & Technology'), ('Others', 'Others')], default='Others', max_length=50),
        ),
    ]
