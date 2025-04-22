import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import Movie  # Replace 'app' with your actual app name

TMDB_API_BASE = "https://api.themoviedb.org/3"

def fetch_tmdb_poster(title, api_key=None, access_token=None):
    headers = {
        "Authorization": f"Bearer {access_token}"
    } if access_token else {}

    params = {
        "query": title,
        "api_key": api_key,
    }

    response = requests.get(f"{TMDB_API_BASE}/search/movie", headers=headers, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    results = data.get("results")
    if results:
        poster_path = results[0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

class Command(BaseCommand):
    help = 'Fetch missing movie posters from TMDb using movie titles'

    def handle(self, *args, **kwargs):
        api_key = getattr(settings, 'TMDB_API_KEY', None)
        access_token = getattr(settings, 'TMDB_ACCESS_TOKEN', None)

        if not api_key and not access_token:
            self.stdout.write(self.style.ERROR("TMDB_API_KEY or TMDB_ACCESS_TOKEN not found in settings."))
            return

        movies = Movie.objects.filter(poster_path__in=[None, '', 'N/A'])
        updated = 0

        for movie in movies:
            poster = fetch_tmdb_poster(movie.title, api_key=api_key, access_token=access_token)
            if poster:
                movie.poster_path = poster
                movie.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"✅ Updated: {movie.title}"))
            else:
                self.stdout.write(f"❌ No poster found for: {movie.title}")

        self.stdout.write(self.style.SUCCESS(f"🎉 Done! Posters updated: {updated}"))
