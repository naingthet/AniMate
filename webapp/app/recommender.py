import pandas as pd
from surprise import Dataset, Reader, SVD, dump

ratings_path = 'app/data/clean_data/ratings.csv'
svd_params = {'n_epochs': 50, 'lr_all': 0.01, 'reg_all': 0.1}
model_path = 'app/algo/svd_model'


def recommender(ratings_path, svd_params):
    # Load data
    data = pd.read_csv(ratings_path)
    # Prepare data for algorithm
    reader = Reader(rating_scale=(1, 10))
    dataset = Dataset.load_from_df(data[['user_id', 'anime_id', 'rating']], reader)
    #trainset, _ = train_test_split(dataset, test_size=0.0)
    trainset = dataset.build_full_trainset()
    # Initialize and train model
    algo = SVD(**svd_params)
    algo.fit(trainset)
    return algo


if __name__ == '__main__':
    model = recommender(ratings_path=ratings_path, svd_params=svd_params)
    dump.dump(model_path, algo=model)
    print("Model Successfully Trained and Saved")
