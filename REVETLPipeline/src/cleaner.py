import regex as rx
from .logger import logger

def clean(data):
    data["YEAR"] = data["YEAR"].str.replace(r"–", "-", regex=True)
    data["YEAR"] = data["YEAR"].str.replace("- ", "-Present", regex=True)
    
    logger.info('source=movies.csv rows= %s path=/data/movies.csv - Year column format changed from "(%%YYYY- )" to "(%%YYYY-Present)" for shows still running', len(data))
    temp = len(data)
    data = data.drop_duplicates(subset=["MOVIES"])
    logger.info('source=movies.csv rows= %s path=/data/movies.csv - Number of rows dropped = %s', len(data), temp - len(data))
    print(data.index.name)
    print(data.head())