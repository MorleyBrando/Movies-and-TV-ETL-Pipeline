import os
import psycopg2
from logger import logger


def load(data, dupes, unkownStars):
    conn = psycopg2.connect(
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD", ""),
        host=os.getenv("PG_HOST"),
        port=int(os.getenv("PG_PORT", "5432"))
    )
    
    cursor  = conn.cursor()
    
    sql_create = """CREATE TABLE IF NOT EXISTS Movies (
    id SERIAL PRIMARY KEY, 
    Movie TEXT UNIQUE NOT NULL CHECK (length(Movie) BETWEEN 1 AND 120),
    year TEXT,       
    Genre TEXT, 
    Rating NUMERIC(2,1),
    One_Line TEXT,
    Stars TEXT,
    Votes TEXT,
    Runtime INT,
    Gross TEXT);"""
            
    cursor.execute(sql_create)
    conn.commit()
    
    for _, row in data.iterrows():
        
        sql_insert = """
        INSERT INTO Movies (Movie, year, Genre, Rating, One_line, Stars, Votes, Runtime, Gross) 
        Values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (Movie) DO NOTHING;
        """
        cursor.execute(sql_insert, (row['MOVIES'], row['YEAR'], row['GENRE'], row['RATING'], row['ONE-LINE'], row['STARS'], row['VOTES'], row['RunTime'], row['Gross']))
        conn.commit()  
        
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: Data loaded into Movies table in Postgres', len(data))
  
    
    cursor.execute("""
                   SELECT EXISTS(
                       SELECT 1
                       FROM information_schema.tables
    					WHERE table_name = 'dupes');
                       """)
    exists = cursor.fetchone()[0]
    
    if not exists:
        sql_create = """CREATE TABLE IF NOT EXISTS Dupes( 
        Movie TEXT,
        Year TEXT,       
        Genre TEXT, 
        Rating NUMERIC(2,1),
        One_Line TEXT,
        Stars TEXT,
        Votes TEXT,
        Runtime INT,
        Gross TEXT);"""
        
        cursor.execute(sql_create)
        conn.commit()

        for _, row in dupes.iterrows():
            
            sql_insert = """
            INSERT INTO Dupes (Movie, year, Genre, Rating, One_line, Stars, Votes, Runtime, Gross) 
            Values (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(sql_insert, (row['MOVIES'], row['YEAR'], row['GENRE'], row['RATING'], row['ONE-LINE'], row['STARS'], row['VOTES'], row['RunTime'], row['Gross']))
            conn.commit()
        logger.info('source=movies.csv rows= %s path=/data/movies.csv: Duplicate data loaded into Dupes table in Postgres', len(data))
            
    else:
        logger.info('source=movies.csv rows= %s path=/data/movies.csv: Duplicate data was not loaded into Dupes table in Postgres because dupes table already created', len(data))
        
        
    sql_create = """CREATE TABLE IF NOT EXISTS "Unknown Stars"(
    Movie TEXT UNIQUE REFERENCES Movies(Movie),
    year TEXT,       
    Genre TEXT, 
    Rating NUMERIC(2,1),
    One_Line TEXT,
    Stars TEXT,
    Votes TEXT,
    Runtime INT,
    Gross TEXT);"""
            
    cursor.execute(sql_create)
    conn.commit()
    
    for _, row in unkownStars.iterrows():
            
        sql_insert = """
        INSERT INTO "Unknown Stars"(Movie, year, Genre, Rating, One_line, Stars, Votes, Runtime, Gross) 
        Values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (Movie) DO NOTHING;
        """
        cursor.execute(sql_insert, (row['MOVIES'], row['YEAR'], row['GENRE'], row['RATING'], row['ONE-LINE'], row['STARS'], row['VOTES'], row['RunTime'], row['Gross']))
        conn.commit()  
            
    conn.close()
    