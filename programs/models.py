import uuid
from accounts.models import User
from django.db import models


class Event(models.Model):
    EVENT_CATEGORIES = [
        ('Arts', 'Arts'),
        ('Business', 'Business'),
        ('Enterpreneurship', 'Enterpreneurship'),
        ('Education', 'Education'),
        ('Fashion', 'Fashion'),
        ('Film', 'Film'),
        ('Food', 'Food'),
        ('Politics', 'Politics'), 
        ('Health', 'Health'),
        ('Music', 'Music'),
        ('Science & Technology', 'Science & Technology'),
        ('Others', 'Others')
    ]


    id = models.CharField(max_length=9, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    category= models.CharField(max_length=50, choices=EVENT_CATEGORIES, default='Others')
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    image = models.ImageField(default='default.jpg', upload_to='event_images')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.name}'


    def save(self, *args, **kwargs):
        if not self.id:
            self.id = 'ev-' + str(uuid.uuid4())[:6]
        super().save(*args, **kwargs)

    
    class Meta:
        ordering = ('-created_at',)