# from django.db import models
# from django.contrib.auth.models import User

# class Genre(models.Model):
#     name = models.CharField(max_length=100, unique=True)
    
#     def __str__(self):
#         return self.name

# class Movie(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     release_year = models.IntegerField(default=2000)
#     genres = models.ManyToManyField(Genre)
    
#     # Add fields needed for ML model prediction
#     budget = models.FloatField(null=True, blank=True)
#     runtime = models.FloatField(null=True, blank=True)
#     vote_average = models.FloatField(null=True, blank=True)
#     vote_count = models.IntegerField(null=True, blank=True)
#     poster_path = models.URLField(max_length=500, null=True, blank=True, default='N/A')
    
#     def __str__(self):
#         return self.title

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     interested_genres = models.ManyToManyField(Genre, blank=True)
    
#     def __str__(self):
#         return f"{self.user.username}'s profile"
    
from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.IntegerField(default=2000)
    genres = models.ManyToManyField(Genre)
    
    # Fields used by ML model
    budget = models.FloatField(null=True, blank=True)
    runtime = models.FloatField(null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)
    
    # Additional TMDB fields that could be useful
    popularity = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    tagline = models.TextField(blank=True, null=True)
    poster_path = models.URLField(max_length=500, null=True, blank=True, default='N/A')
    
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interested_genres = models.ManyToManyField(Genre, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"