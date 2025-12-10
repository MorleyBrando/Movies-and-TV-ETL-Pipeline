import os
import psycopg2
from logger import logger


def load(data, tv, cleanMovie, cleanTv):
    conn = psycopg2.connect(
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD", ""),
        host=os.getenv("PG_HOST"),
        port=int(os.getenv("PG_PORT", "5432"))
    )
    
    cursor  = conn.cursor()
    
    #Creating bronze_movies table if it does not exist
    sql_create = """CREATE TABLE IF NOT EXISTS bronze_movies(
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
    
    #Entering data into bronze_movies table
    for _, row in data.iterrows():    
        sql_insert = """
        INSERT INTO bronze_movies(Movie, year, Genre, Rating, One_line, Stars, Votes, Runtime, Gross) 
        Values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (Movie) DO NOTHING;
        """
        cursor.execute(sql_insert, (row['MOVIES'], row['YEAR'], row['GENRE'], row['RATING'], row['ONE-LINE'], row['STARS'], row['VOTES'], row['RunTime'], row['Gross']))
        conn.commit()  
        
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: Data loaded into Movies table in Postgres', len(data))
    
    #Checking if bronze_duplicates table exists
    cursor.execute("""
                   SELECT EXISTS(
                       SELECT 1
                       FROM information_schema.tables
    					WHERE table_name = %s);
                       """, ("bronze_duplicates",))
    exists = cursor.fetchone()[0]
    
    #Creating bronze_duplicates table and entering data if it does not exist
    if not exists:
        sql_create = """CREATE TABLE IF NOT EXISTS bronze_duplicates( 
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

        for _, row in tv.iterrows():
            
            sql_insert = """
            INSERT INTO bronze_duplicates(Movie, year, Genre, Rating, One_line, Stars, Votes, Runtime, Gross) 
            Values (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(sql_insert, (row['MOVIES'], row['YEAR'], row['GENRE'], row['RATING'], row['ONE-LINE'], row['STARS'], row['VOTES'], row['RunTime'], row['Gross']))
            conn.commit()
        logger.info('source=movies.csv rows= %s path=/data/movies.csv: Duplicate Data loaded into bronze_duplicates.', len(data))
            
    else:
        logger.info('source=movies.csv rows= %s path=/data/movies.csv: Duplicate Data not loaded into bronze_duplicates.', len(data))
    
    #Creating silver_movies table if it does not exist
    sql_create = """CREATE TABLE IF NOT EXISTS silver_movies(
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
    
    #Entering data into silver_movies table
    for _, row in cleanMovie.iterrows():     
        sql_insert = """
        INSERT INTO silver_movies(Movie, year, Genre, Rating, One_line, Stars, Votes, Runtime, Gross) 
        Values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (Movie) DO NOTHING;
        """
        cursor.execute(sql_insert, (row['MOVIES'], row['YEAR'], row['GENRE'], row['RATING'], row['ONE-LINE'], row['STARS'], row['VOTES'], row['RunTime'], row['Gross']))
        conn.commit()  
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: Clean Movie data loaded into silver_movies table in Postgres', len(data))

    #Checking if silver_duplicates table exists     
    cursor.execute("""
                   SELECT EXISTS(
                       SELECT 1
                       FROM information_schema.tables
    					WHERE table_name = %s);
                       """, ("silver_duplicates",))
    exists = cursor.fetchone()[0]
    
    #Creating silver_duplicates table and entering data if it does not exist
    if not exists:
        sql_create = """CREATE TABLE IF NOT EXISTS silver_duplicates(
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
        
        for _, row in cleanTv.iterrows():
            
            sql_insert = """
            INSERT INTO silver_duplicates(Movie, year, Genre, Rating, One_line, Stars, Votes, Runtime, Gross) 
            Values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (Movie) DO NOTHING;
            """
            cursor.execute(sql_insert, (row['MOVIES'], row['YEAR'], row['GENRE'], row['RATING'], row['ONE-LINE'], row['STARS'], row['VOTES'], row['RunTime'], row['Gross']))
            conn.commit()
        logger.info('source=movies.csv rows= %s path=/data/movies.csv: Duplicate data loaded into silver_duplicates table in Postgres', len(data)) 
    else:
        logger.info('source=movies.csv rows= %s path=/data/movies.csv: Duplicate data was not loaded into silver_duplicates table in Postgres because silver_duplicates table already created.', len(data))    
        
    logger.info('source=movies.csv rows= %s path=/data/movies.csv: All Tables data were loaded.', len(data))
    conn.close()