import sqlite3
import pandas as pd
import exceptions


class Database:
    def __init__(self, dbname="flats_db"):
        self.dbname = dbname
        try:
            self.conn = sqlite3.connect(dbname)
        except exceptions.db_connect_fail as e:
            print(f"connect to database failed {e}")
        self.cursor = self.conn.cursor()
        self.PREPARED_JSON = "prepared_items_df.json"

    def setup(self):
        query = """
                --DROP TABLE IF EXISTS items;
                CREATE TABLE IF NOT EXISTS items(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                rating REAL,            time TEXT, 
                price INTEGER,          address TEXT, 
                subway TEXT,            minutes_to_subway INTEGER,
                rooms INTEGER,          total_area REAL, 
                living_area REAL,       kitchen_area REAL, 
                balcony TEXT,           type_of_renovation TEXT,
                type_of_house TEXT,     link TEXT,
                cur_floor INTEGER,      cnt_floors INTEGER,
                shown INTEGER )"""
        self.conn.execute(query)
        # self.cursor.executescript(query)  # recreated table until test
        self.conn.commit()

    def add_parsed_items(self, column_values: pd.DataFrame, table: str = "items"):
        columns = ", ".join(column_values.columns)
        values = [tuple(value) for value in column_values.values]
        self.cursor.executemany(
            f"INSERT INTO {table} ({columns}) VALUES ({','.join('?' * len(column_values.columns))})",
            values,
        )
        self.conn.commit()

    def get_top_five(self):
        """Get top five items"""

        query = """SELECT t.link FROM items t
                WHERE t.shown is Null
                ORDER BY t.rating DESC
                LIMIT 5"""
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return [x[0] for x in result]  # Убрать x

    def update_shown_cards(self, links, table="items"):
        query = f"""UPDATE {table}
                SET shown = 1
                WHERE link in {tuple(links)}"""
        self.cursor.execute(query)
        self.conn.commit()

    def get_all_items(self, table="items"):
        query = f"""SELECT * FROM {table} t"""
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def check_if_link_exist(self, added_values: list, table="items"):
        query = (
            f"""SELECT t.link FROM {table} t WHERE t.link in {tuple(added_values)}"""
        )
        self.cursor.execute(query)
        result = [links[0] for links in self.cursor.fetchall()]
        return result

    def get_duplicates(self, table="items"):
        query = f"""SELECT COUNT(DISTINCT(t.link)), COUNT(*) FROM {table} t"""
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def delete_duplicates(self, table="items"):
        pass

    def get_cards_to_predict(self) -> pd.DataFrame:
        """Get items without rating"""

        query = "SELECT * FROM table t WHERE t.rating = Null"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    #### NON CHECKED FUNCTION!###
    def replace_estimated_cards(
        self, column_values: pd.DataFrame, table: str = "items"
    ):
        columns = ", ".join(column_values.columns)
        values = [tuple(value) for value in column_values.values]
        self.cursor.executemany(
            f"REPLACE INTO {table} ({columns}) VALUES({','.join('?' * len(column_values.columns))}",
            values,
        )
        self.conn.commit()
