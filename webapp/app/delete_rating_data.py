from app.models import Ratings
from app import db

''' 
Delete rating data from SQLAlchemy database (only use when importing new data)
'''

def delete_rating_data():
    ratings = Ratings.query.all()
    for rating in ratings:
        db.session.delete(rating)
    db.session.commit()

if __name__ == '__main__':
    delete_rating_data()
    print("Rating data deleted")