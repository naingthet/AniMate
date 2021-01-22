from app.models import Ratings
from app import db
import json

''' 
WARNING: Do not uncomment and run this file unless absolutely necessary, as it will delete all stored user ratings
Delete rating data from SQLAlchemy database (only use when importing new data)
'''


def delete_rating_data():
    ratings = Ratings.query.all()
    for rating in ratings:
        db.session.delete(rating)
    db.session.commit()


''' 
Seed new, cleaned ratings data into the SQLAlchemy database
'''

data_path = 'app/data/clean_data/ratings.json'


def load_ratings_data(filename):
    """Load anime information from a json file into the database."""
    with open(filename) as f:
        json_data = json.load(f)
        for rating in json_data:
            ratings = Ratings(
                anime_id=rating['anime_id'], anime_name=rating['name'],
                user_rating=rating['rating'], user_id=rating['user_id']
                )
            db.session.add(ratings)
        db.session.commit()


if __name__ == '__main__':
    delete_rating_data()
    print("Rating data deleted")
    load_ratings_data(data_path)
    print('Rating data seeded successfully')
