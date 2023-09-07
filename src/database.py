import sqlite3
import pandas as pd
import src.exceptions as exc
from typing import NamedTuple
import cfg


class TopFlat(NamedTuple):
    link: str
    price: int
    subway: str
    item_id: int


class Database:
    def __init__(self, dbname=cfg.PATH_TO_DB):
        self.dbname = dbname
        try:
            self.conn = sqlite3.connect(self.dbname)
        except Exception as err:
            raise exc.DBConnectionFailed from err
        self.cursor = self.conn.cursor()

    def insert_flat(self, column_values: pd.DataFrame, table: str = "items"):
        columns = ", ".join(column_values.columns)
        values = [tuple(value) for value in column_values.values]
        try:
            self.cursor.executemany(
                f"INSERT INTO {table} ({columns}) VALUES ({','.join('?' * len(column_values.columns))})",
                values,
            )
            self.conn.commit()
        except Exception as err:
            raise exc.AddToDBFailed from err

    def get_flat_with_max_rating(self) -> TopFlat:
        """Get top item from database"""

        query = """SELECT t.link, t.price, t.subway, t.id
                FROM items t
                WHERE t.shown is Null
                ORDER BY t.rating DESC
                LIMIT 1"""
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return TopFlat(link=result[0], price=result[1], subway=result[2], item_id=result[3])

    def set_is_ad_shown(self, item_id, table="items"):
        query = f"""UPDATE {table}
                SET shown = 1
                WHERE id = {item_id}"""
        self.cursor.execute(query)
        self.conn.commit()

    def get_all_items(self, table="items") -> pd.DataFrame:
        """Select all items from database"""
        query = f"""SELECT * FROM {table} t;"""
        df = pd.read_sql(query, self.conn)
        return df

    def get_not_estimated_items(self, table="items") -> pd.DataFrame:
        """Select non estimated items from database"""
        query = f"""SELECT * FROM {table} t
                WHERE t.rating is Null;"""
        df = pd.read_sql(query, self.conn)
        return df

    def is_link_exist(self, added_values: list, table="items"):
        query = (
            f"""SELECT t.link FROM {table} t WHERE t.link in {tuple(added_values)}"""
        )
        self.cursor.execute(query)
        result = [links[0] for links in self.cursor.fetchall()]
        return result

    def get_duplicates(self, table="items"):
        query = f"""SELECT COUNT(DISTINCT(t.link)), COUNT(*) FROM {table} t"""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_duplicates(self, table="items"):
        query = f"""
                DELETE FROM {table}
                WHERE rowid NOT IN (
                SELECT MIN(rowid) 
                FROM {table}
                GROUP BY link
                )
                """
        self.cursor.execute(query)
        self.conn.commit()

    def update_flat_rating(self, estimated_df: pd.DataFrame, table: str = "items"):
        try:
            estimated_df.to_sql('temp_table', self.conn, if_exists='replace')  # create temp table with rating
            query = f"""
                    UPDATE {table}
                    SET rating = (SELECT t.rating FROM temp_table t WHERE t.id = {table}.id)
                    WHERE id in (SELECT t.id FROM temp_table t)                    
                    """
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as err:
            raise exc.UpdateDBItemsFailed from err

