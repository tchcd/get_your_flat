import sqlite3
import pandas as pd
import exceptions


class Database:
    def __init__(self, dbname='flats_db'):
        self.dbname = dbname
        try:
            self.conn = sqlite3.connect(dbname)
        except exceptions.db_connect_fail as e:
            print(f'connect to database failed {e}')
        self.cursor = self.conn.cursor()
        self.PREPARED_JSON = 'prepared_items_df.json'

    def setup(self):
        query = """
                DROP TABLE IF EXISTS items;
                CREATE TABLE IF NOT EXISTS items(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                rating REAL,            time TEXT, 
                price INTEGER,          address TEXT, 
                subway TEXT,            distance_to_subway INTEGER,
                rooms INTEGER,          total_area REAL, 
                living_area REAL,       kitchen_area REAL, 
                balcony TEXT,           type_of_renovation TEXT,
                type_of_house TEXT,     link TEXT,
                cur_floor INTEGER,      cnt_floors INTEGER,
                shown INTEGER)"""
        # self.conn.execute(query)
        self.cursor.executescript(query)  # recreated table until test
        self.conn.commit()

    def add_parsed_items(self, column_values: pd.DataFrame, table: str = 'items'):
        columns = ', '.join(column_values.columns)
        values = [tuple(value) for value in column_values.values]
        self.cursor.executemany(
            f"INSERT INTO {table} ({columns}) VALUES ({','.join('?' * len(column_values.columns))})", values
        )
        self.conn.commit()

    def get_top_five(self):
        """Забирает топ-5 объявлений"""
        query = """SELECT t.link FROM items t
                WHERE t.shown is Null
                ORDER BY t.rating DESC
                LIMIT 5"""
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return [x[0] for x in result]

    def update_shown_cards(self, links, table='items'):
        lns = "','".join(links)
        print(lns)
        query = f"""UPDATE {table}
                SET shown = 1
                WHERE link in {tuple(links)}"""

        self.cursor.execute(query)
        self.conn.commit()

    def get_all_items(self, table='items'):
        query = f"""SELECT * FROM {table} t"""
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_duplicates(self, table='items'):
        query = f"""SELECT COUNT(DISTINCT(t.link)), COUNT(*) FROM {table} t"""
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def delete_duplicates(self, table='items'):
        pass

    def get_cards_to_predict(self):
        """Достает новые, не размеченные объявления, для МЛ алгоритма"""
        # query = "SELECT * FROM table t WHERE t.rating = Null"
        pass

    def update_predicted_cards(self):
        """Обновляет рейтинг после предсказания Мл алгоритма"""
        pass
