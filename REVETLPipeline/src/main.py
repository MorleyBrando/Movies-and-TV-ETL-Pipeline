from .csv_reader import csv_reader
from .validator import validate
from .cleaner import clean
from .loader import load
import os
import psycopg2
from .logger import logger

def run_pipeline():
    
    logger.info("STARTING ETL")
    data = csv_reader()
    data = validate(data)
    clean(data)
    load(data)
    
run_pipeline()

