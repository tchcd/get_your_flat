# Это модуль подготовки данных после получения из пасрсера
import logging
from logcfg import logger_cfg
import exceptions
import pandas as pd
from sklearn.impute import KNNImputer
from datetime import date, timedelta
import dataenforce
import json
from test import raw

logging.config.dictConfig(logger_cfg)
log_error = logging.getLogger('log_error')
log_info = logging.getLogger('log_info')


# ПРОБЛЕМА В ТОМ ЧТО СТОЛБЫ ИНТЫ ОТОБРАЖЕНЫ КАК СТР
# ПРОПУЩЕННЫЕ ЗНАЧЕНИЯ СПЛИТ 0 ЛИСТ ОФ РЕЙНДЖ
# НЕ ВЫТАСКИВАЕТСЯ ТАЙМ, ДИСТАНС
# ВОПРОС УДАЛЯЕТ ЛИ ВООБЩЕ NANы ИЗ _prepare_subway


# Create DataFrame
def _prepare_dataframe(raw_data_from_parser: list) -> pd.DataFrame:
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
        "Жилая площадь",
        "Площадь кухни",
        "Этаж",
        "Балкон или лоджия",
        "Ремонт",
        "Вид сделки",
        "Тип дома",
        "Запланирован снос",
        "link",
    ]

    main_df = pd.DataFrame(columns=cols).append(raw_data_from_parser)[cols]
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
        "living_area",
        "kitchen_area",
        "floor",
        "balcony",
        "type_of_renovation",
        "type_of_deal",
        "type_of_house",
        "demolition_plan",
        "link",
    ]
    return main_df


# Time prepare
def _time_changer(time):
    """This function converts time values and uses them in the _prepare_time func"""
    if time[0].lower() == "вчера":
        yesterday = date.today() - timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")
    elif time[0].lower() == "сегодня":
        yesterday = date.today() - timedelta(days=0)
        return yesterday.strftime("%Y-%m-%d")
    else:
        return "-".join(time)


def _prepare_time(df):
    """This function makes correct time column"""
    df["time"] = df["time"].apply(lambda x: _time_changer(x))
    return df["time"]


# Subway / Distance to subway
def _prepare_subway(df):
    """Remove NaN-values from subway and distance_to_subway columns, and makes a correct distance column"""
    df = df[~df["subway"].isna()].copy()
    df = df[~df["minutes_to_subway"].isna()].copy()
    return df[["subway", "minutes_to_subway"]]


# Area
def _round_area(obj):
    first_value = int(obj.split()[0].split(".")[0])
    second_value = int(obj.split()[0].split(".")[-1])
    if second_value >= 5:
        return first_value + 1
    else:
        return first_value


def _prepare_area(df):
    df["total_area"] = df["total_area"].apply(lambda x: x.split()[0].split(".")[0])
    df["kitchen_area"] = df["kitchen_area"].apply(
        lambda x: int(x.split()[0].split(".")[0]) + 1
        if int(x.split()[0].split(".")[-1]) >= 5
        else int(x.split()[0].split(".")[0])
    )
    df["living_area"] = df["living_area"].apply(
        lambda x: _round_area(x) if pd.notnull(x) else x
    )
    return df[["total_area", "kitchen_area", "living_area"]]


def _prepare_floors(df):
    df["floor"] = df["floor"].apply(lambda x: x.split())
    df["cur_floor"] = df["floor"].apply(lambda x: x[0]).astype(int)
    df["cnt_floors"] = df["floor"].apply(lambda x: x[-1]).astype(int)
    return df


def _drop_columns(df):
    df = df.loc[df["demolition_plan"] != "да"].copy()
    df = df[
        (df["type_of_deal"]).isna() | (df["type_of_deal"] == "возможна ипотека")
        ].copy()
    df = df[df["cnt_floors"] != "1"].copy()
    df = df.loc[df["cnt_floors"] != df["cur_floor"]].copy()

    df = df.drop("demolition_plan", axis=1)
    df = df.drop("type_of_deal", axis=1)
    df = df.drop("floor", axis=1)

    return df


def _fill_nan(df):
    df.loc[df["type_of_renovation"].isna(), "type_of_renovation"] = "неизвестно"
    df.loc[df["balcony"].isna(), "balcony"] = "нет"
    return df


def prepare_parsed_card(raw_data: list) -> pd.DataFrame:
    """Prepare clean dataframe after raw parser
    :param raw_data: raw list of dictionaries after parsing
    :return: Updated Dataframe
    """
    imputer = KNNImputer(n_neighbors=3)
    try:
        log_info.info('START PARSED DATA PREPARING')
        df = _prepare_dataframe(raw_data)
        df["time"] = _prepare_time(df)
        df[["subway", "minutes_to_subway"]] = _prepare_subway(df)
        df[["total_area", "kitchen_area", "living_area"]] = _prepare_area(df)
        df[["total_area", "living_area", "kitchen_area"]] = imputer.fit_transform(
            df[["total_area", "living_area", "kitchen_area"]]
        )
        df = _prepare_floors(df)
        df = _drop_columns(df)
        df = _fill_nan(df)
        log_info.info('STOP PARSED DATA PREPARING')
    except:
        raise exceptions.prepare_data_failed('DATA PREPARATION FAILED')

    return df


def get_not_duplicated_items(df: pd.DataFrame, db_name) -> pd.DataFrame:
    """Check if links exist in database and return dataframe with not existed items"""
    links_to_add = df["link"].values
    duplicated_links = db_name.check_if_link_exist(links_to_add)
    ready_to_add_links = set(links_to_add) - set(duplicated_links)

    return df[df["link"].isin(ready_to_add_links)]


if __name__ == "__main__":
    raw_d = prepare_parsed_card(raw)
