from csv_reader import csv_reader
from validator import validate
from cleaner import clean
from loader import load
from logger import logger

def run_pipeline():
    
    logger.info("STARTING ETL")
    data = csv_reader()
    data = validate(data)
    data = clean(data)
    
    load(data[0], data[1], data[2])
    
run_pipeline()

