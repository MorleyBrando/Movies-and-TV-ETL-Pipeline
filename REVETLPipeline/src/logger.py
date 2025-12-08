import logging 
import os 

if os.path.exists('etl.log'):
    os.remove('etl.log')


logger = logging.getLogger("ETL")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('etl.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

