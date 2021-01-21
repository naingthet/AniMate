import pandas as pd
from surprise import Dataset, Reader, SVD, dump

model_path = 'app/algo/svd_model'


def make_recommendations(test_data, model=model_path):

    # Load trained model
    _, algo = dump.load(model)

    # Read in user rating data
    reader = Reader(rating_scale=(1, 10))
    dataset = Dataset.load_from_df(test_data[['user_id', 'anime_id', 'rating']], reader)

    #
