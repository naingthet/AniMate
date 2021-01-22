import pandas as pd

"""Load, preprocess, and export cleaned rating data. Rating data will be merged with anime data. """

rating_raw = 'data/raw_data/raw_rating.csv'
anime_clean = 'data/clean_data/anime.csv'


def load_data(filename):
    """Load data into pandas dataframes"""
    data = pd.read_csv(filename)
    return data

def preprocess_rating(rating_df, anime_df, frac=0.1):
    """
    Clean, preprocess, and return rating dataframe.
    """
    # Drop rows where rating = -1 and duplicates
    ratings = rating_df[rating_df['rating'] != -1]
    ratings = ratings.drop_duplicates()
    # Adding 10,000 to each user_id to ensure that there is no overlap with the site's users
    ratings['user_id'] = ratings['user_id'].apply(lambda x: x+10000)
    # Rename anime id column for merging dataframes
    animes = anime_df.rename(columns={"id": "anime_id"})
    # Merge datasets
    data = pd.merge(ratings, animes, how='left', on='anime_id', suffixes=['_user', '_avg'])
    data = data.drop_duplicates()
    data = data.dropna()
    # Sample a subset of the data to reduce file size
    data = data.sample(frac=frac)
    return data


# Full preprocessing using defined functions
def export_clean_ratings(rating_raw, anime_clean):
    # Load dataframes
    rating_df = load_data(rating_raw)
    anime_df = load_data(anime_clean)
    ratings = preprocess_rating(rating_df=rating_df, anime_df=anime_df)
    ratings.to_csv('data/clean_data/ratings.csv', index=False)


if __name__ == '__main__':
    export_clean_ratings(rating_raw, anime_clean)
    print("Ratings Data Preprocessed Successfully")