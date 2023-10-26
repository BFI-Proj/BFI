from django.db import models


# Create your models here.

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('prefer_not_to_say', 'Prefer Not to Say'),
    ]

    full_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=11)
    password = models.CharField(max_length=128)  # Assuming you are storing hashed passwords
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)

    def __str__(self):
        return self.username
    
def upload_to_img_directory(instance, filename):
    # This function defines the subdirectory within your MEDIA_ROOT/img
    # where uploaded images will be stored. Uploaded files will be in the MEDIA_ROOT/img folder.
    return f'img/{filename}'

class YourModel(models.Model):
    image = models.ImageField(upload_to=upload_to_img_directory)

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    category = models.CharField(max_length=255, default="Uncategorized")  # Add a default value
    image = models.ImageField(upload_to='img/', default='', blank=False, null=False)
    description = models.TextField(default="No Description")  # Add a description field

    def __str__(self):
        return self.name
    
    # models.py


