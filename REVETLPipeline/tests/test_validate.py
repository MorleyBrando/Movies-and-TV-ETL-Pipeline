import pytest 
import pandas as pd

import sys
import os

# Add REVETLPipeline folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.validator import validate

def test_validate_null_values():
    # Creating a sample DataFrame with NULL values
    data = pd.DataFrame({
        'MOVIES': ['Movie1', 'Movie2', "Movie3", None],
        'YEAR': ["(2020)", None, "(2019)", None],
        'GENRE': ['Action', None, 'Comedy', None],
        'RATING': [8.5, 7.0, None, None],
        'ONE-LINE': ['Great movie', 'Good movie', None, None],
        'STARS': ['Star1, Star2', None, 'Star3', None],
        'VOTES': ['1,000', None, '500', None],
        'RunTime': [120, None, 90, None],
        'Gross': ['$100M', None, '$50M', None]
    })
    
    
    # Validating the data
    validated_data = validate(data)
    
    print(validated_data)
    
    # Checking if NULL values are replaced correctly
    assert validated_data['MOVIES'].isnull().sum() == 0
    assert validated_data['YEAR'].isnull().sum() == 0
    assert validated_data['GENRE'].isnull().sum() == 0
    
    # Checking specific replacements
    assert validated_data.loc[1, 'YEAR'] == "Unkown"
    assert validated_data.loc[1, 'GENRE'] == "Unkown"
    assert validated_data.loc[2, 'RATING'] == 0
    assert validated_data.loc[2, 'ONE-LINE'] == "Unkown"
    assert validated_data.loc[1, 'STARS'] == "Unkown"
    assert validated_data.loc[1, 'VOTES'] == 0
    assert validated_data.loc[1, 'RunTime'] == 0
    assert validated_data.loc[1, 'Gross'] == 0
    assert len(validated_data) == 3  # One row with NULL MOVIES should be removed