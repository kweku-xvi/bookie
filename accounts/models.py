import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from PIL import Image


class MyUserManager(BaseUserManager):
    def create_user(self,email,password:None,**extra_fields):
        if not email:
            raise ValueError(_("Email is required."))
        email = self.normalize_email(email=email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("SuperUser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("SuperUser must have is_superuser=True"))
        return self.create_user(email,password,**extra_fields)


class User(AbstractUser):
    id = models.CharField(max_length=8, primary_key=True, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_of_birth = models.DateField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'date_of_birth']


    def __str__(self):
        return f'{self.username}'

    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    
    class Meta:
        ordering = ('-created_at',)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    

    def __str__(self):
        return f"{self.user.username}'s Profile"

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)