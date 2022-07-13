import sqlite3
import pandas as pd
import exceptions
from typing import Dict, List, NamedTuple


class flat_data(NamedTuple):
    rating = float
    time = str
    price = int
    address = str
    subway = str
    distance_to_subway = int
    rooms = int or str
    total_area = float
    living_area = float
    kitchen_area = float
    balcony = str
    type_of_renovation = str
    type_of_house = str
    link = str
    cur_floor = int
    cnt_floors = int
    shown = bool


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
        #self.conn.execute(query)
        self.cursor.executescript(query)  # recreated table until test
        self.conn.commit()

    def add_parsed_items(self, column_values: pd.DataFrame, table: str = 'items'):
       columns = ', '.join(column_values.columns)
       values = [tuple(value) for value in column_values.values]
       self.cursor.executemany(
           f"INSERT INTO {table} ({columns}) VALUES ({','.join('?' * len(column_values.columns))})", values
       )
       self.conn.commit()

    def send_top_to_telegram(self):
        """Забирает топ-5 объявлений"""
        query = """SELECT t.link FROM items t
                WHERE t.shown = 0
                ORDER BY t.rating DESC
                LIMIT 5"""
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
        # return [x for x in self.conn.execute(query)]
        # дальше можно распарсить и вернуть

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

    def add_daily_avito_cards_to_db(self):
        """Отправляет в SQL подготовленные новые данные после ежедневного парсера"""
        # query = insert all new data
        pass

    def get_cards_to_predict(self):
        """Достает новые, не размеченные объявления, для МЛ алгоритма"""
        # query = "SELECT * FROM table t WHERE t.rating = Null"
        pass

    def update_predicted_cards(self):
        """Обновляет рейтинг после предсказания Мл алгоритма"""
        pass
