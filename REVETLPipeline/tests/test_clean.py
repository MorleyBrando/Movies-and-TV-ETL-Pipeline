import pytest 
import pandas as pd
import sys
import os

# Add REVETLPipeline folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.cleaner import clean
    # Creating a sample DataFrame
data = pd.DataFrame({
    'MOVIES': ['Movie1', 'Movie2', 'Movie3'],
    'YEAR': ['(2020)', '2021', '(2020- )'],
    'GENRE': ['Action', 'Comedy', 'Drama'],
    'RATING': [8.5, 7.0, 9.0],
    'ONE-LINE': ['Great movie', 'Good movie', 'Add a Plot'],
    'STARS': ['Star1, Star2', 'Star3, Star4', ' '],
    'VOTES': ['1,000', '500', '2,000'],
    'RunTime': [120, 90, 150],
    'Gross': ['$100M', '$50M', '$150M']
})

def test_clean_year_column():
    
    # Cleaning the data
    cleaned_data = clean(data)[0]
    
    # Checking if YEAR column is cleaned correctly
    assert cleaned_data.loc[0, 'YEAR'] == '(2020)'
    assert cleaned_data.loc[1, 'YEAR'] == '2021'
    assert cleaned_data.loc[2, 'YEAR'] == '(2020-Present)'  # N/A should be converted to 0
    
def test_clean_votes_column():
    
    # Cleaning the data
    cleaned_data = clean(data)[0]
    
    # Checking if VOTES column is cleaned correctly
    assert cleaned_data.loc[0, 'VOTES'] == '1000'
    assert cleaned_data.loc[1, 'VOTES'] == '500'
    assert cleaned_data.loc[2, 'VOTES'] == '2000'
    
def test_clean_stars_and_one_line_columns():
    # Cleaning the data
    cleaned_data = clean(data)[0]
    
    # Checking if STARS and ONE-LINE columns are cleaned correctly
    assert cleaned_data.loc[0, 'STARS'] == 'Star1, Star2'
    assert cleaned_data.loc[1, 'STARS'] == 'Star3, Star4'
    assert cleaned_data.loc[2, 'STARS'] == 'Unknown'
    
    assert cleaned_data.loc[0, 'ONE-LINE'] == 'Great movie'
    assert cleaned_data.loc[1, 'ONE-LINE'] == 'Good movie'
    assert cleaned_data.loc[2, 'ONE-LINE'] == 'Unknown'
    
def test_clean_separating_tv_shows():
    # Cleaning the data
    movie, tv_data, cleanMovie, cleanTv = clean(data)
    
    # Checking if TV shows are separated correctly
    assert len(tv_data) == 0  # No duplicates in sample data
    assert len(cleanMovie) == 2  # All rows should remain in movie dataset