import uuid
from accounts.models import User
from django.db import models
from PIL import Image


class Event(models.Model):
    EVENT_CATEGORIES = [
        ('arts', 'Arts'),
        ('business', 'Business'),
        ('concert', 'Concert'),
        ('education', 'Education'),
        ('fashion', 'Fashion'),
        ('film', 'Film'),
        ('health', 'Health'),
        ('music', 'Music'),
        ('politics', 'Politics'), 
        ('scienceandtechnology', 'Science & Technology'),
        ('others', 'Others')
    ]


    id = models.CharField(max_length=9, primary_key=True, unique=True)
    name = models.CharField(max_length=255, unique=True)
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.CharField(max_length=255)
    category= models.CharField(max_length=50, choices=EVENT_CATEGORIES, default='Others')
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    image = models.ImageField(default='default.jpg', upload_to='event_images')
    is_active = models.BooleanField(default=False)
    organized_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.name}'


    def save(self, *args, **kwargs):
        if not self.id:
            self.id = 'ev-' + str(uuid.uuid4())[:6]
        super().save(*args, **kwargs)


    
    class Meta:
        ordering = ('-created_at',)
