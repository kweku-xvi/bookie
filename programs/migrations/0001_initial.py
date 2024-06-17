# Generated by Django 4.2.1 on 2024-06-17 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.CharField(max_length=6, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('categories', models.CharField(choices=[('Arts', 'Arts'), ('Business', 'Business'), ('Enterpreneurship', 'Enterpreneurship'), ('Education', 'Education'), ('Fashion', 'Fashion'), ('Film', 'Film'), ('Food', 'Food'), ('Politics', 'Politics'), ('Health', 'Health'), ('Music', 'Music'), ('Science & Technology', 'Science & Technology'), ('Others', 'Others')], default='Others', max_length=50)),
                ('event_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('image', models.ImageField(default='default.jpg', upload_to='event_images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
