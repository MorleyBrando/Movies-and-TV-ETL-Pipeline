import pandas as pd 
from logger import logger

def csv_reader():
    
    movies = pd.read_csv("REVETLPipeline/data/movies.csv")
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: CSV file data read', len(movies))
    
    return movies