import pandas as pd 
from .logger import logger

def csv_reader():
    
    movies = pd.read_csv("/Users/brandomorley/Documents/Revature/RevPractice/Week1/Day1/REVETLPipeline/data/movies.csv")
    logger.info('source=movies.csv rows= %s path=/data/movies.csv', len(movies))
    print(movies.tail(6))
    
    
    return movies