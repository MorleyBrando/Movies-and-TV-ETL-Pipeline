from logger import logger

def clean(data):
    #Cleaning Year Column
    data["YEAR"] = data["YEAR"].str.replace(r"–", "-", regex=True)
    data["YEAR"] = data["YEAR"].str.replace("- ", "-Present", regex=True)
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: Year column format changed from "(%%YYYY- )" to "(%%YYYY-Present)" for shows still running', len(data))
    
    #Cleaning Rating Column
    data.loc[:,"VOTES"] = data["VOTES"].str.replace(",", "")
    data.loc[:, "VOTES"] = data["VOTES"].fillna(0)
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: Votes changed from String to Integer Values', len(data))
    
    #Cleaning Stars and One-Line Columns
    data.loc[:, 'STARS'] = data['STARS'].str.strip()
    data.loc[data['STARS'] == '', 'STARS'] = 'Unknown'
    
    data.loc[:, 'ONE-LINE'] = data['ONE-LINE'].str.strip()
    data.loc[data['ONE-LINE'] == 'Add a Plot', 'ONE-LINE'] = 'Unknown'
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: ', len(data))
    
    #Seperating TV Shows from Movies
    temp = len(data)
    tv = data[data.duplicated(subset=['MOVIES'], keep=False)]
    data = data.drop_duplicates(subset=["MOVIES"], keep=False)
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: New Dataset of TV Shows created. Length of TV dataset = %s', len(tv), len(tv))
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: Number of rows dropped = %s', len(data), temp - len(data))
    
    #Cleaning Movie Dataset 
    cleanMovie = data.loc[data['STARS'] != 'Unknown', :]
    cleanMovie = cleanMovie.loc[cleanMovie['RATING'] != 0, :]
    cleanMovie = cleanMovie.loc[cleanMovie['ONE-LINE'] != 'Unknown', :]
    cleanMovie = cleanMovie.loc[cleanMovie['RunTime'] != 0, :]
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: Cleaned Movie dataset created by removing rows with Unknown Stars, 0 Ratings, Unknown One-Line, and 0 RunTime', len(cleanMovie))
    
    #Cleaning Duplicate Dataset
    cleanTv = tv.loc[tv['STARS'] != 'Unknown', :]
    cleanTv = cleanTv.loc[cleanTv['RATING'] != 0, :]
    cleanTv = cleanTv.loc[cleanTv['ONE-LINE'] != 'Unknown', :]
    cleanTv = cleanTv.loc[cleanTv['RunTime'] != 0, :]
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: Cleaned TV dataset created by removing rows with Unknown Stars, 0 Ratings, Unknown One-Line, and 0 RunTime', len(cleanTv))
    
    return (data, tv, cleanMovie, cleanTv)
    