import pandas as pd
import re

'''
Load, preprocess, and export cleaned anime data. These functions will preprocess anime data, passed as pandas dataframe. 
Our anime data has columns ['anime_id', 'name', 'genre', 'type' 'episodes', 'rating', 'members'].
This script must be run from the "app" directory.
'''

rating_raw = 'data/raw_data/raw_rating.csv'
anime_clean = 'data/clean_data/anime.csv'
anime_raw = 'data/raw_data/raw_anime.csv'

def load_data(filename):
    """Load data into pandas dataframes"""
    data = pd.read_csv(filename)
    return data


# Utility Functions

def explicit(genre):
    """Detect explicit animes based on genre"""

    if 'Hentai' in genre:
        return 'Yes'
    else:
        return 'No'

def pick_most_popular(data, frac):
    """ Function that will limit data to the most popular animes"""

    data = data.sort_values('members', ascending=False)
    max_row = round(len(data) * frac)
    data = data.iloc[:max_row, :]

    return data


def text_cleaner(text):
    # Use regular expressions to remove punctutation, nonstandard characters, and web links
    text = text.replace('&#039;', "'")
    text = text.replace('&quot;', '"')
    text = re.sub(r"[^{L}\w%\s:,!()\-&]", '', text)
    text = text.strip()
    return text


# Preprocessing data

def preprocess_anime(anime_df, frac=0.1):
    """Preprocess anime data"""

    # Remove rows with missing genre and rating
    anime_df = anime_df.dropna(axis=0, subset=['genre', 'rating'])

    # Remove explicit animes
    anime_df['explicit'] = anime_df['genre'].apply(explicit)
    anime_df = anime_df[anime_df['explicit'] == 'No']
    anime_df = anime_df.drop('explicit', 1)

    # Pick the top n% most popular animes
    anime_df = pick_most_popular(anime_df, frac)

    # Clean the anime names
    anime_df['name'] = anime_df['name'].apply(text_cleaner)

    # Clean up the dataframes
    anime_df = anime_df.reset_index().drop(['index'], axis=1)
    anime_df = anime_df.reset_index()
    anime_df = anime_df.drop(['anime_id'], axis=1)
    anime_df = anime_df.rename(columns={
        'index': 'id',
        'rating': 'avg_rating'
    })

    return anime_df


# Full preprocessing using defined functions
def export_clean_anime(filename):
    anime_df = load_data(filename)
    anime_df = preprocess_anime(anime_df)

    anime_df.to_json('data/clean_data/anime.json', orient='records')
    anime_df.to_csv('data/clean_data/anime.csv', index=False)
    anime_df[['id', 'name']].to_csv('data/clean_data/anime_ids.csv', index=False)


"""Load, preprocess, and export cleaned rating data. Rating data will be merged with anime data. """


def preprocess_rating(rating_df, anime_df, frac=0.05):
    """
    Clean, preprocess, and return rating dataframe
    """
    # Drop rows where rating = -1 and duplicates
    ratings = rating_df[rating_df['rating'] != -1].drop_duplicates()

    # Rank users by number of ratings (for sampling)
    users = ratings.groupby('user_id')['rating'].count().reset_index().sort_values(ascending=False, by='rating')

    # # Select top n% of users to reduce file size
    # users = users.iloc[:int(len(users) * frac)]

    # Randomly sample n% of users to reduce file size
    users = users.sample(frac=frac)

    # Select ratings from top users
    ratings = ratings[ratings['user_id'].isin(users['user_id'].values)]

    # Adding 10,000 to each user_id to ensure that there is no overlap with the site's users
    ratings['user_id'] = ratings['user_id'].apply(lambda x: x + 10000)
    # Rename anime id column for merging dataframes
    animes = anime_df.rename(columns={"id": "anime_id"})
    # Merge datasets
    data = pd.merge(ratings, animes, how='left', on='anime_id', suffixes=['_user', '_avg']).drop_duplicates().dropna()

    # #Sample a subset of the data to reduce file size
    # data = data.sample(frac=frac)

    return data


# Full preprocessing using defined functions
def export_clean_ratings(rating_raw, anime_clean):
    # Load dataframes
    rating_df = load_data(rating_raw)
    anime_df = load_data(anime_clean)
    ratings = preprocess_rating(rating_df=rating_df, anime_df=anime_df)
    ratings.to_csv('data/clean_data/ratings.csv', index=False)
    ratings.to_json('data/clean_data/ratings.json', orient='records')


if __name__ == '__main__':
    export_clean_anime(anime_raw)
    print("Anime Data Cleaned Successfully")
    export_clean_ratings(rating_raw, anime_clean)
    print("Ratings Data Preprocessed Successfully")
