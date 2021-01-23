# Initialize elasticsearch indices for a database
from app import app
from app.search import add_to_index, query_index
from app.models import Animes, Ratings

for anime in Animes.query.all():
    add_to_index('animes', anime)
#
# # Query the index
# query_index('animes', 'one punch man', 1, 100)
#
# # Delete the index
# app.elasticsearch.indices.delete('animes')

# Easier way of searching
Animes.reindex()
# query, total = Animes.search('one punch man', 1, 5)
# print(total)
# print(query.all())

# # Data for each query
# user_id = 1
# # user = User.query.get(user_id)
# # user_ratings = user.ratings.all()
# search_ratings = []
#
# for i in query:
#     anime_name = i.name
#     user_rating = Ratings.query.filter_by(anime_name=anime_name, user_id=user_id).first()
#     if user_rating:
#         search_ratings.append(user_rating.user_rating)
#     else:
#         search_ratings.append(None)
# print(search_ratings)
#
#
# # Add some Ratings
# index = len(Ratings.query.all())
# r = Ratings(id=index, anime_name="One Punch Man", user_rating=10, user_id=1)
# db.session.add(r)
# db.session.commit()

