import json
from app import db
import pandas as pd
from app.models import Ratings

''' 
Seed my anime ratings into the database for testing
'''

# Exporting
def export_user_ratings():
    ratings = Ratings.query.filter_by(user_id=1).all()
    user_ratings = [[i.user_id, i.anime_id, i.anime_name, i.user_rating] for i in ratings]
    user_ratings = pd.DataFrame(user_ratings, columns=['user_id', 'anime_id', 'anime_name', 'user_rating'])
    user_ratings.to_json('app/data/example.json', orient='records')
    user_ratings.to_csv('app/data/example.csv', index=False)

# Importing from json
def seed_examples():
    with open('app/data/example.json') as f:
        json_data = json.load(f)
        for rating in json_data:
            ratings = Ratings(
                anime_id=rating['anime_id'], anime_name=rating['anime_name'],
                user_rating=rating['user_rating'], user_id=rating['user_id']
                )
            db.session.add(ratings)
        db.session.commit()

if __name__ == '__main__':
    seed_examples()
    print('Test data seeded successfully')
