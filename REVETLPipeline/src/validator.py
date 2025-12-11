from logger import logger
def validate(data):
    
    #Removing rows where MOVIE is NULL
    data = data[data['MOVIES'].notnull()]
    
    #Validating NULL Values
    data.loc[:, 'YEAR'] = data['YEAR'].fillna("Unknown")
    data.loc[:, 'GENRE'] = data['GENRE'].fillna("Unknown")
    data.loc[:, 'ONE-LINE'] = data['ONE-LINE'].fillna("Unknown")
    data.loc[:, 'STARS'] = data['STARS'].fillna("Unknown")
    data = data.fillna(0)
    
    
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: Gave NULL values a value', len(data))
    return data
    
    
    