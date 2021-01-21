import pandas as pd
import re

'''
Load, preprocess, and export cleaned anime data. These functions will preprocess anime data, passed as pandas dataframe. Our anime data has columns ['anime_id', 'name', 'genre', 'type' 'episodes', 'rating', 'members'].
'''

anime_raw = 'data/raw_data/raw_anime.csv'


def load_data(filename):
    '''Load data into pandas dataframes'''

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
    ''' Function that will limit data to the most popular animes'''

    data = data.sort_values('members', ascending=False)
    max_row = round(len(data) * frac)
    data = data.iloc[:max_row, :]

    return data


def text_cleaner(text):
    # Use regular expressions to remove punctutation, nonstandard characters, and web links
    text = text.replace('&#039;', "'")
    text = text.replace('&quot;', '"')
    text = re.sub(r"[^{L}\w%\s\:\,\!()\-\&]", '', text)
    text = text.strip()
    return text


# Preprocessing data

def preprocess_anime(anime_df):
    '''Preprocess anime data'''

    # Select animes with at least 100 views
    anime_df = anime_df[anime_df['members'] > 100]

    # Remove rows with missing genre and rating
    anime_df = anime_df.dropna(axis=0, subset=['genre', 'rating'])

    # Remove explicit animes
    anime_df['explicit'] = anime_df['genre'].apply(explicit)
    anime_df = anime_df[anime_df['explicit'] == 'No']
    anime_df = anime_df.drop('explicit', 1)

    # Pick the top 10% most popular animes
    anime_df = pick_most_popular(anime_df, 0.1)

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


if __name__ == '__main__':
    export_clean_anime(anime_raw)
    print("Anime Data Cleaned Successfully")
