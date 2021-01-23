import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import numpy as np
from app.models import Ratings, Animes

def predict_ratings(user_id):
    anime_ids_path = 'app/data/clean_data/anime_ids.csv'

    # Query all ratings from database
    total_ratings = Ratings.query.all()

    # Shape data for models
    total_ratings = pd.DataFrame(
        [[i.user_id, i.anime_id, i.user_rating] for i in total_ratings],
        columns=['user_id', 'anime_id', 'rating', ]
    )

    # Surprise reader object
    reader = Reader(rating_scale=(1, 10))

    # Load into trainset
    trainset = Dataset.load_from_df(total_ratings, reader).build_full_trainset()

    # Train the model
    svd_params = {'n_epochs': 50, 'lr_all': 0.01, 'reg_all': 0.1}
    algo = SVD(**svd_params, random_state=310)
    algo.fit(trainset)

    # Find all unique animes
    anime_df = pd.read_csv(anime_ids_path)
    anime_ids = anime_df['id'].to_numpy()

    # Find animes rated by user
    animes_rated_by_user = total_ratings[total_ratings['user_id'] == user_id]['anime_id'].to_numpy()

    # Animes that the user has yet to rate
    animes_to_predict = np.setdiff1d(anime_ids, animes_rated_by_user)

    # Shape user testset with dummy variables for rating (will be replaced with predictions)
    test = [[user_id, anime_id, 0] for anime_id in animes_to_predict]

    # Surprise dataset object
    test_dataset = Dataset.load_from_df(pd.DataFrame(test), reader)

    # Create a testset for predictions
    _, testset = train_test_split(test_dataset, test_size=1.0, shuffle=False)

    # Make predictions
    predictions = algo.test(testset)
    pred_ratings = [i.est for i in predictions]

    # Create a df
    user_predictions = pd.DataFrame((zip(animes_to_predict, pred_ratings)), columns=['anime_id', 'match'])

    # Top 20 recommendations
    user_predictions = user_predictions.sort_values('match', ascending=False).iloc[:20]

    # Use a dictionary to match anime id with name
    name_id_key = dict(anime_df.values)
    user_predictions['anime_name'] = user_predictions['anime_id'].apply(lambda x: name_id_key.get(x))
    user_predictions['match'] = user_predictions['match'].apply(lambda x: round(x*10, 1))
    user_predictions = user_predictions.to_dict(orient='records')

    return user_predictions
