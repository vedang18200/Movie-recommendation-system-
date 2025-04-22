# Place this file in yourapp/management/commands/import_tmdb.py

import json
import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Movie, Genre  # Replace 'movies' with your app name

class Command(BaseCommand):
    help = 'Import movies from TMDB dataset CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the TMDB movies CSV file')
        parser.add_argument('--limit', type=int, default=None, help='Limit the number of movies to import')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        limit = options['limit']
        
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file}'))
            return
            
        self.stdout.write(self.style.SUCCESS(f'Importing TMDB movies from {csv_file}'))
        
        try:
            # Process in a transaction for better performance and consistency
            with transaction.atomic():
                with open(csv_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    
                    counter = {'success': 0, 'error': 0}
                    
                    for row in reader:
                        try:
                            # Check if we've hit the limit
                            if limit and counter['success'] >= limit:
                                break
                                
                            title = row.get('title', '').strip()
                            if not title:
                                self.stdout.write(self.style.WARNING(f"Skipping row with no title"))
                                counter['error'] += 1
                                continue
                            
                            # Extract fields with sensible defaults
                            try:
                                release_year = int(row.get('release_date', '2000')[:4])
                            except (ValueError, IndexError):
                                release_year = 2000
                                
                            try:
                                budget = float(row.get('budget', 0))
                            except (ValueError, TypeError):
                                budget = 0
                                
                            try:
                                runtime = float(row.get('runtime', 0))
                            except (ValueError, TypeError):
                                runtime = 0
                                
                            try:
                                vote_average = float(row.get('vote_average', 0))
                            except (ValueError, TypeError):
                                vote_average = 0
                                
                            try:
                                vote_count = int(float(row.get('vote_count', 0)))
                            except (ValueError, TypeError):
                                vote_count = 0
                            
                            # Get a decent-sized description
                            description = row.get('overview', '').strip()
                            if not description:
                                description = f"No description available for {title}"
                                
                            # Create or update movie
                            movie, created = Movie.objects.update_or_create(
                                title=title,
                                defaults={
                                    'description': description,
                                    'release_year': release_year,
                                    'budget': budget,
                                    'runtime': runtime,
                                    'vote_average': vote_average,
                                    'vote_count': vote_count,
                                    'poster_path': f"https://image.tmdb.org/t/p/w500{row.get('poster_path', '')}" if row.get('poster_path') else 'N/A',
                                    'popularity': float(row.get('popularity', 0)),
                                    'revenue': float(row.get('revenue', 0)),
                                    'tagline': row.get('tagline', '')
                                }
                            )
                            
                            # Add genres (parse from JSON)
                            if 'genres' in row and row['genres']:
                                try:
                                    genres_data = json.loads(row['genres'].replace("'", '"'))
                                    for genre_item in genres_data:
                                        genre_name = genre_item.get('name')
                                        if genre_name:
                                            genre, _ = Genre.objects.get_or_create(name=genre_name)
                                            movie.genres.add(genre)
                                except json.JSONDecodeError:
                                    self.stdout.write(self.style.WARNING(f"Could not parse genres for {title}"))
                            
                            status = "Created" if created else "Updated"
                            self.stdout.write(f"{status} movie: {title}")
                            counter['success'] += 1
                            
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"Error processing {row.get('title', 'Unknown')}: {str(e)}"))
                            counter['error'] += 1
                    
                self.stdout.write(self.style.SUCCESS(f"Import completed. Success: {counter['success']}, Errors: {counter['error']}"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Fatal error during import: {str(e)}"))