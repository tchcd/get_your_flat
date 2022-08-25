from cfg import PATH_TO_DB
import sqlite3


# Initial setup database
def db_initialize():
    dbname = PATH_TO_DB
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = """
            --DROP TABLE IF EXISTS items;
            CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            rating REAL,            time TEXT, 
            price INTEGER,          sqmeter_price INTEGER,
            address TEXT,           subway TEXT,            
            rooms INTEGER,          minutes_to_subway INTEGER,
            total_area REAL,
            balcony TEXT,           type_of_renovation TEXT,
            type_of_house TEXT,     link TEXT,
            cur_floor INTEGER,      cnt_floors INTEGER,
            shown INTEGER )"""
    conn.execute(query)
    cursor.executescript(query)  # recreated table for test
    conn.commit()


if __name__ == "__main__":
    db_initialize()
