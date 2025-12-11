from logger import logger
def validate(data):
    
    #Removing rows where MOVIE is NULL
    data = data[data['MOVIES'].notnull()]
    
    #Validating NULL Values
    data.loc[:, 'YEAR'] = data['YEAR'].fillna("Unkown")
    data.loc[:, 'GENRE'] = data['GENRE'].fillna("Unkown")
    data.loc[:, 'ONE-LINE'] = data['ONE-LINE'].fillna("Unkown")
    data.loc[:, 'STARS'] = data['STARS'].fillna("Unkown")
    data = data.fillna(0)
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: Gave NULL values a value', len(data))
    return data
    
    
    