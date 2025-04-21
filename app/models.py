from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.IntegerField(default=2000)  # Add default value here
    genres = models.ManyToManyField(Genre)
    
    def __str__(self):
        return self.title
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interested_genres = models.ManyToManyField(Genre, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"