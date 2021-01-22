from app.models import Animes
from app import db

''' 
Delete anime data from SQLAlchemy database (only use when importing new data)
'''


def delete_anime_data():
    animes = Animes.query.all()
    for anime in animes:
        db.session.delete(anime)
    db.session.commit()


if __name__ == '__main__':
    delete_anime_data()
    print("Anime data deleted")
