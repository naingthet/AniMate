import json
from app import db
from app.models import Animes, Ratings

''' 
Delete anime data from SQLAlchemy database (only use when importing new data)
'''


def delete_anime_data():
    animes = Animes.query.all()
    for anime in animes:
        db.session.delete(anime)
    db.session.commit()


''' 
Seed new, cleaned anime data into the SQLAlchemy database
'''


data_path = 'app/data/clean_data/anime.json'


def load_anime_info(filename):
    """Load anime information from a json file into the database."""
    with open(filename) as f:
        json_data = json.load(f)
        for anime in json_data:
            animes = Animes(
                id=anime['id'], name=anime['name'],
                genre=anime['genre'], type=anime['type'],
                episodes=anime['episodes'],
                avg_rating=anime['avg_rating'], members=anime['members'])
            db.session.add(animes)
        db.session.commit()


if __name__ == '__main__':
    delete_anime_data()
    print("Anime data deleted")
    load_anime_info(data_path)
    print('Anime data seeded successfully')
