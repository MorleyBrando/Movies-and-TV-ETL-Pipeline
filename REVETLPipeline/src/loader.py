import os
import psycopg2


def load(data):
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
    Rating FLOAT,
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
    conn.close()
    