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

@login_required
def recommend_movies(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    selected_genres = profile.interested_genres.all()
    
    if not selected_genres:
        return redirect('select_genres')
    
    # Use genre names to search for movies
    movies = []
    api_key = "c82df010"  # Your OMDb API key
    
    # Make one API call per genre to get recommendations
    for genre in selected_genres:
        response = requests.get(
            f"http://www.omdbapi.com/?apikey={api_key}&type=movie&s={genre.name}&page=1"
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True' and 'Search' in data:
                # For each movie result, get more details
                for item in data['Search'][:3]:  # Limit to 3 movies per genre
                    movie_id = item['imdbID']
                    movie_details = requests.get(
                        f"http://www.omdbapi.com/?apikey={api_key}&i={movie_id}"
                    ).json()
                    
                    if movie_details.get('Response') == 'True':
                        movies.append({
                            'title': movie_details['Title'],
                            'description': movie_details.get('Plot', 'No description available.'),
                            'release_year': movie_details.get('Year', 'Unknown'),
                            'poster_path': movie_details.get('Poster', 'N/A'),
                            'genre': movie_details.get('Genre', ''),
                            'rating': movie_details.get('imdbRating', 'N/A')
                        })
    
    # Remove duplicates based on title
    unique_movies = []
    titles = set()
    for movie in movies:
        if movie['title'] not in titles:
            titles.add(movie['title'])
            unique_movies.append(movie)
    
    return render(request, 'recommendations.html', {
        'movies': unique_movies,
        'selected_genres': selected_genres
    })