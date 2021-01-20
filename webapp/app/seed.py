import json
from app.models import Animes 
from app import db

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

