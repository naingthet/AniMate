import json
from app import db
from app.models import Animes, Ratings

filename = 'data/clean_data/anime.json'
filename = 'app/data/clean_data/anime.json'

def load_anime_info(filename):
    """Load anime information from a json file into the database."""
    with open(filename) as f:
        json_data = json.load(f)
        for anime in json_data:
            animes = Animes(
                id = anime['id'], name = anime['name'],
                genre = anime['genre'], type = anime['type'],
                episodes = anime['episodes'],
                avg_rating = anime['avg_rating'], members = anime['members'])
            db.session.add(animes)
        db.session.commit()

if __name__ == '__main__':
    load_anime_info(filename)
    print('Anime Data Loaded Successfully')
