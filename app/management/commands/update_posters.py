import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import Movie  # Replace 'app' with your actual app name

def fetch_omdb_poster(title, api_key):
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    response = requests.get(url).json()

    if response.get("Response") == "True" and response.get("Poster") != "N/A":
        return response["Poster"]
    return None

class Command(BaseCommand):
    help = 'Fetch missing movie posters from OMDb using movie titles'

    def handle(self, *args, **kwargs):
        api_key = getattr(settings, 'OMDB_API_KEY', None)

        if not api_key:
            self.stdout.write(self.style.ERROR("OMDB_API_KEY not found in settings."))
            return

        movies = Movie.objects.filter(poster_path__in=[None, '', 'N/A'])
        updated = 0

        for movie in movies:
            poster = fetch_omdb_poster(movie.title, api_key)
            if poster:
                movie.poster_path = poster
                movie.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"✅ Updated: {movie.title}"))
            else:
                self.stdout.write(f"❌ No poster found for: {movie.title}")

        self.stdout.write(self.style.SUCCESS(f"🎉 Done! Posters updated: {updated}"))
