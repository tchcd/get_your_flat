# Это модуль подготовки данных после получения из пасрсера
import logging
from src.logcfg import logger_cfg
import pandas as pd
from datetime import date, timedelta, datetime
import dataenforce

logging.config.dictConfig(logger_cfg)
log_error = logging.getLogger('log_error')
log_info = logging.getLogger('log_info')


class DataPreparation:
    #def __init__(self, raw_data):
    #    self.data = raw_data

    def _create_df(self, raw_data: list) -> pd.DataFrame:
        """This function create and prepare working dataframe with objects from parser"""
        cols = [
            "rating",
            "shown",
            "time",
            "price",
            "address",
            "subway",
            "minutes_to_subway",
            "Количество комнат",
            "Общая площадь",
            "Этаж",
            "Балкон или лоджия",
            "Ремонт",
            "Вид сделки",
            "Тип дома",
            "Запланирован снос",
            "link"
        ]

        main_df = pd.DataFrame(columns=cols).append(raw_data)[cols]
        main_df.columns = [
            "rating",
            "shown",
            "time",
            "price",
            "address",
            "subway",
            "minutes_to_subway",
            "rooms",
            "total_area",
            "floor",
            "balcony",
            "type_of_renovation",
            "type_of_deal",
            "type_of_house",
            "demolition_plan",
            "link"
        ]
        return main_df

    @staticmethod
    def _time_changer(time: list) -> str:
        """This function converts time values and uses them in the _prepare_time func"""

        time = time.split('·')
        all_months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
                      'августа', 'сентября', 'октября', 'ноября', 'декабря']

        if 'вчера' in time:
            yesterday = date.today() - timedelta(days=1)
            return yesterday.strftime("%Y-%m-%d")
        elif 'сегодня' in time:
            yesterday = date.today() - timedelta(days=0)
            return yesterday.strftime("%Y-%m-%d")
        else:
            day = time.text.lower().split('·')[1].strip().split()[:2][0]
            month = str(all_months.index(time.text.lower().split('·')[1].strip().split()[:2][1]) + 1)
            if len(month) == 1:
                month = f"0{month}"
            year = str(datetime.now().year)
            return '-'.join([year, month, day])

    def _prepare_time(self, df: pd.DataFrame) -> pd.DataFrame:
        """Makes correct time column"""
        df["time"] = df["time"].apply(lambda x: self._time_changer(x))
        return df

    def _prepare_subway(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove NaN-values from subway and distance_to_subway columns, and makes a correct distance column"""
        df = df[~df["subway"].isna()]
        df = df[~df["minutes_to_subway"].isna()]
        return df

    def _prepare_area(self, df):
        """Makes correct area column"""
        df["total_area"] = df["total_area"].apply(lambda x: str(x).split()[0].split(".")[0]).astype('float')
        return df

    def _prepare_floors(self, df: pd.DataFrame) -> pd.DataFrame:
        """Makes correct floors column"""
        df["floor"] = df["floor"].apply(lambda x: str(x).split())
        df["cur_floor"] = df["floor"].apply(lambda x: x[0]).astype(int)
        df["cnt_floors"] = df["floor"].apply(lambda x: x[-1]).astype(int)
        return df

    def _drop_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drops unused columns"""
        df = df.loc[df["demolition_plan"] != "да"]
        df = df[
            (df["type_of_deal"]).isna() | (df["type_of_deal"] == "возможна ипотека")
            ]
        df = df[df["cnt_floors"] != "1"]
        df = df.loc[df["cnt_floors"] != df["cur_floor"]]

        df = df.drop("demolition_plan", axis=1)
        df = df.drop("type_of_deal", axis=1)
        df = df.drop("floor", axis=1)

        return df

    def _fill_nan(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fills rows witn NaN"""
        df.loc[df["type_of_renovation"].isna(), "type_of_renovation"] = "неизвестно"
        df.loc[df["balcony"].isna(), "balcony"] = "нет"
        return df

    def _check_valid_columns(self, raw_data: list) -> list:
        """checks if the required keys exists in the raw items"""
        need_keys = ['time', 'price', "subway", "minutes_to_subway",
                     "Количество комнат", "Общая площадь", "Этаж"]
        raw_data = [valid for valid in raw_data if
                    not need_keys - valid.keys()]
        return raw_data

    def start_preparing(self, raw_data: list) -> pd.DataFrame:
        """Prepares clean dataframe from the raw data
        :param raw_data: list of dictionaries
        :return: cleaned Dataframe
        """
        log_info.info('START PARSED DATA PREPARING')
        valid_items = self._check_valid_columns(raw_data)
        df = self._create_df(valid_items)
        df = self._prepare_time(df)
        df = self._prepare_subway(df)
        df = self._prepare_area(df)
        df = self._prepare_floors(df)
        df = self._drop_columns(df)
        df = self._fill_nan(df)
        df['sqmeter_price'] = df['price'] // df['total_area']
        df["rooms"].astype(int)
        df = df.drop_duplicates('link')
        log_info.info('STOP PARSED DATA PREPARING')

        return df