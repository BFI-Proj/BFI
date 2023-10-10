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

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.name
