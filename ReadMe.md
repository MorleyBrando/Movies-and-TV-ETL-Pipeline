# Basic ETL Pipeline 
## Movies and TV Shows

This is a basic ETL Pipeline that is meant to extract the Movies and TV dataset from a csv. Transform the dataset so that values are formatted well and not NULL. Load the fixed dataset into a Postgres Database that can be viewed in DBeaver.

## Project Structure
```python
Movies-and-TV-ETL-Pipeline/
|- REVETLPipeline
   |- data 
      |- movies.csv
   |- src
       |- cleaner.py
       |- confiq.py
       |- csv_reader.py
       |- loader.py
       |- logger.py
       |- main.py
       |- validator.py
   |-ReadMe.md
   |- requirements.txt
   |- etl.log
```

## How To Start
```
python3 -m venv path/to/venv
source path/to/venv/bin/activate #macOS/Linux
.\.venv\Scripts\activate        # Windows
python3 -m pip install -r requirements.txt
python3 ./REVETLPipeline/src/main.py 
```

## Tech Stack
- Python
- PostgreSQL
- Pandas
- Pycopg2
- Logging
