import pandas as pd
import numpy as np
from surprise import Reader, dump

def recommend():
    model_path = 'app/algo/svd_model'
    anime_ids_path = 'app/data/clean_data/anime_ids.csv'

    # Load trained model
    _, algo = dump.load(model_path)

    # Read in user rating data
    reader = Reader(rating_scale=(1, 10))

    # Create a dataframe of user's ratings
    user_id = current_user.id
    query = Ratings.query.filter_by(user_id=user_id).all()
    ratings = [[user_id, i.anime_id, i.user_rating] for i in query]
    rating_df = pd.DataFrame(ratings, columns=['user_id', 'anime_id', 'rating'])

    # Identify the animes the user has not seen yet
    anime_df = pd.read_csv(anime_ids_path)
    anime_ids = anime_df['id'].to_numpy()
    animes_rated_by_user = rating_df['anime_id'].values
    animes_to_predict = np.setdiff1d(anime_ids, animes_rated_by_user)
    name_id_key = dict(anime_df.values)

    # Create user testset and predict
    user_testset = [[user_id, anime_id, None] for anime_id in animes_to_predict]
    predictions = algo.test(user_testset)
    pred_ratings = np.array([pred.est for pred in predictions])

    user_predictions = pd.DataFrame((zip(animes_to_predict, pred_ratings*10)), columns=['anime_id', 'match'])
    user_predictions = user_predictions.sort_values('match', ascending=False).iloc[:20]
    user_predictions['anime_name'] = user_predictions['anime_id'].apply(lambda x: name_id_key.get(x))
    user_predictions['match'] = user_predictions['match'].apply(lambda x: round(x, 1))
    user_predictions = user_predictions.to_dict(orient='records')

    return render_template('recommend.html', user_predictions=user_predictions)
