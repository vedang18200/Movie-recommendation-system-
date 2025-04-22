from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Genre, UserProfile
from .forms import GenreSelectionForm, CustomSignupForm
from django.contrib.auth import login
from django.db.models import Count, Q  
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Genre
from django.contrib.auth import login, logout


# Landing Page (Public)
def landing_page(request):
    return render(request, 'base.html')

def logout_view(request):
    logout(request)
    return redirect('landing_page')

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            # Create user but don't save yet
            user = form.save(commit=False)
            # Set password manually since we're handling it in our custom form
            user.set_password(form.cleaned_data['password'])
            # Now save the user
            user.save()
            login(request, user)
            return redirect('home_page')
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})

# Home Page (After Login)
@login_required
def home_page(request):
    return render(request, 'home.html')

# Select Genres
@login_required
def select_genres(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = GenreSelectionForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('recommend_movies')
    else:
        form = GenreSelectionForm(instance=profile)

    return render(request, 'select_genres.html', {'form': form})

# Recommend Movies Based on Selected Genres
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Movie, Genre, UserProfile
import joblib
import numpy as np
import os
from django.db.models import Q
@login_required
def recommend_movies(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    selected_genres = profile.interested_genres.all()

    if not selected_genres:
        return redirect('select_genres')

    # Define default poster URL - do this at the beginning so it's available in both success and error cases
    default_poster_url = '/static/images/poster.png'

    # Load model and scaler
    try:
        model_path = os.path.join(settings.BASE_DIR, 'models/best_model.pkl')
        scaler_path = os.path.join(settings.BASE_DIR, 'models/scaler.pkl')
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
    except Exception as e:
        return render(request, 'recommendations.html', {
            'error': f"Error loading ML model: {str(e)}",
            'movies': [],
            'selected_genres': selected_genres,
            'default_poster_url': default_poster_url
        })

    # Find movies that have at least one of the selected genres
    # This will give more recommendations but keep them relevant
    movies = Movie.objects.filter(genres__in=selected_genres).distinct()
    
    # Filter to only movies with complete feature data
    movies = movies.exclude(
        Q(budget__isnull=True) | 
        Q(runtime__isnull=True) | 
        Q(vote_average__isnull=True) | 
        Q(vote_count__isnull=True)
    )
    
    recommended_movies = []
    
    # Prepare features for batch prediction
    features_list = []
    movie_list = []
    
    for movie in movies:
        features = [movie.budget, movie.runtime, movie.vote_average, movie.vote_count]
        features_list.append(features)
        movie_list.append(movie)
    
    if features_list:  # Check if we have any valid movies
        # Convert to numpy array and scale
        features_array = np.array(features_list)
        features_scaled = scaler.transform(features_array)
        
        # Make predictions for all movies at once
        predictions = model.predict(features_scaled)
        
        # Add movies with positive predictions
        for i, pred in enumerate(predictions):
            if pred == 1:  # Only include popular ones based on SVM prediction
                recommended_movies.append(movie_list[i])
    
    # Sort recommended movies by vote average (as a simple ranking method)
    recommended_movies.sort(key=lambda x: x.vote_average, reverse=True)
    
    # Limit to top 20 recommendations
    recommended_movies = recommended_movies[:20]
    
    return render(request, 'recommendations.html', {
        'movies': recommended_movies,
        'selected_genres': selected_genres,
        'default_poster_url': default_poster_url  # Add this line
    })