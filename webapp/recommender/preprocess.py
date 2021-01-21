import numpy as np
import pandas as pd

# These functions will preprocess anime data, passed as pandas dataframe
# Our anime data has columns ['anime_id', 'name', 'genre', 'type', 'episodes', 'rating', 'members']

def load_data(filename):
    '''
    
