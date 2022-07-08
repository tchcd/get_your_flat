import sqlite3
from typing import Dict, List


class Database:
    def __init__(self, dbname='flat_db'):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def setup(self):
        query = "CREATE TABLE IF NOT EXISTS items"
        self.conn.execute(query)
        self.conn.commit()

    def add_items(self, table: str, column_values: Dict):
        columns = ', '.join(column_values.keys())
        values = [tuple(column_values.values())]
        self.cursor.executemany(
            f"INSERT INTO {table} ({columns}) VALUES ({values})"
        )
        self.conn.commit()

    def get_top_items(self):
        """Забирает топ-5 объявлений"""
        query = "SELECT t.link FROM items t" \
                "WHERE t.showed = 0" \
                "ORDER BY t.evaluate DESC" \
                "LIMIT 5"
        self.cursor.execute(query)
        #result = self.cursor.fetchall()   # вот это надо потестить
        #return [x for x in self.conn.execute(query)]
        # дальше можно распарсить и вернуть

    def add_daily_avito_cards_to_db(self):
        """Отправляет в SQL подготовленные новые данные после ежедневного парсера"""
        # query = insert all new data
        pass

    def get_not_evaluated_cards(self):
        """Достает новые, не размеченные объявления, для МЛ алгоритма"""
        # query = "SELECT * FROM table WHERE evaluate = Null"
        pass
