# save this as populate_db.py in your project directory
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app.models import Movie, Genre  # Adjust 'app' to your actual app name

def create_genres():
    genres = [
        'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
        'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery',
        'Romance', 'Science Fiction', 'Thriller', 'War', 'Western'
    ]
    
    created_genres = []
    for genre_name in genres:
        genre, created = Genre.objects.get_or_create(name=genre_name)
        created_genres.append(genre)
        print(f"Genre {'created' if created else 'exists'}: {genre_name}")
    
    return created_genres

def create_movies(genres):
    # Dictionary mapping genre names to Genre objects for easy access
    genre_dict = {genre.name: genre for genre in genres}
    
    movies_data = [
        {
            'title': 'The Shawshank Redemption',
            'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
            'release_year': 1994,
            'genres': ['Drama']
        },
        {
            'title': 'The Godfather',
            'description': 'An organized crime dynasty\'s aging patriarch transfers control of his clandestine empire to his reluctant son.',
            'release_year': 1972,
            'genres': ['Crime', 'Drama']
        },
        {
            'title': 'The Dark Knight',
            'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
            'release_year': 2008,
            'genres': ['Action', 'Crime', 'Drama', 'Thriller']
        },
        {
            'title': 'Pulp Fiction',
            'description': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
            'release_year': 1994,
            'genres': ['Crime', 'Drama']
        },
        {
            'title': 'Forrest Gump',
            'description': 'The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other historical events unfold through the perspective of an Alabama man with an IQ of 75.',
            'release_year': 1994,
            'genres': ['Drama', 'Romance']
        },
        {
            'title': 'Inception',
            'description': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
            'release_year': 2010,
            'genres': ['Action', 'Adventure', 'Science Fiction', 'Thriller']
        },
        {
            'title': 'The Matrix',
            'description': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
            'release_year': 1999,
            'genres': ['Action', 'Science Fiction']
        },
        {
            'title': 'Spirited Away',
            'description': 'During her family\'s move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.',
            'release_year': 2001,
            'genres': ['Animation', 'Adventure', 'Family', 'Fantasy']
        },
        {
            'title': 'Parasite',
            'description': 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.',
            'release_year': 2019,
            'genres': ['Comedy', 'Drama', 'Thriller']
        },
        {
            'title': 'The Silence of the Lambs',
            'description': 'A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.',
            'release_year': 1991,
            'genres': ['Crime', 'Drama', 'Thriller', 'Horror']
        },
        {
            'title': 'Toy Story',
            'description': 'A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy\'s room.',
            'release_year': 1995,
            'genres': ['Animation', 'Adventure', 'Comedy', 'Family']
        },
        {
            'title': 'Titanic',
            'description': 'A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.',
            'release_year': 1997,
            'genres': ['Drama', 'Romance']
        },
        {
            'title': 'Jurassic Park',
            'description': 'A pragmatic paleontologist visiting an almost complete theme park is tasked with protecting a couple of kids after a power failure causes the park\'s cloned dinosaurs to run loose.',
            'release_year': 1993,
            'genres': ['Adventure', 'Science Fiction', 'Thriller']
        },
        {
            'title': 'The Lion King',
            'description': 'Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.',
            'release_year': 1994,
            'genres': ['Animation', 'Adventure', 'Drama', 'Family']
        },
        {
            'title': 'The Avengers',
            'description': 'Earth\'s mightiest heroes must come together and learn to fight as a team if they are going to stop the mischievous Loki and his alien army from enslaving humanity.',
            'release_year': 2012,
            'genres': ['Action', 'Adventure', 'Science Fiction']
        }
    ]
    
    for movie_data in movies_data:
        movie, created = Movie.objects.get_or_create(
            title=movie_data['title'],
            defaults={
                'description': movie_data['description'],
                'release_year': movie_data['release_year']
            }
        )
        
        # Add genres to the movie
        for genre_name in movie_data['genres']:
            movie.genres.add(genre_dict[genre_name])
        
        status = 'created' if created else 'exists'
        print(f"Movie {status}: {movie.title} ({', '.join(movie_data['genres'])})")

if __name__ == '__main__':
    print("Populating database with sample data...")
    genres = create_genres()
    create_movies(genres)
    print("Done!")