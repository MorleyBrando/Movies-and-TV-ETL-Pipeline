from logger import logger

def clean(data):
    data["YEAR"] = data["YEAR"].str.replace(r"–", "-", regex=True)
    data["YEAR"] = data["YEAR"].str.replace("- ", "-Present", regex=True)
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: Year column format changed from "(%%YYYY- )" to "(%%YYYY-Present)" for shows still running', len(data))
    
    
    data.loc[:,"VOTES"] = data["VOTES"].str.replace(",", "")
    data.loc[:, "VOTES"] = data["VOTES"].fillna(0)
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: Votes changed from String to Integer Values', len(data))
    
    data.loc[:, 'STARS'] = data['STARS'].str.strip()
    data.loc[data['STARS'] == '', 'STARS'] = 'Unknown'
    
    temp = len(data)
    dupes = data[data.duplicated(subset=['MOVIES'])]
    data = data.drop_duplicates(subset=["MOVIES"])
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: Number of rows dropped = %s', len(data), temp - len(data))
    
    unkownStars = data.loc[data['STARS'] == 'Unknown', :]
    
    return (data, dupes, unkownStars)
    