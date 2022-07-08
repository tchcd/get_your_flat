# Это модуль подготовки данных после получения из пасрсера
from typing import NamedTuple
from sklearn.impute import KNNImputer
from datetime import date, timedelta
import pandas as pd
import json

# ПРОБЛЕМА В ТОМ ЧТО СТОЛБЫ ИНТЫ ОТОБРАЖЕНЫ КАК СТР
# ПРОПУЩЕННЫЕ ЗНАЧЕНИЯ СПЛИТ 0 ЛИСТ ОФ РЕЙНДЖ
# НЕ ВЫТАСКИВАЕТСЯ ТАЙМ, ДИСТАНС
# ВОПРОС УДАЛЯЕТ ЛИ ВООБЩЕ NANы ИЗ _prepare_subway


data_test = [{'link': 'https://www.avito.ru/sankt-peterburg/kvartiry/2-k._kvartira_458m_49et._2378275977',
              'price': 8150000, 'address': 'Санкт-Петербург, пр-т Просвещения, 46к2', 'time': '22 06',
              'subway': 'Проспект Просвещения', 'distance_to_subway': '1 км',
              'Тип дома': 'панельный', 'Год постройки': '1975', 'Этажей в доме': '9', 'Пассажирский лифт': '1',
              'Грузовой лифт': 'нет', 'В доме': 'мусоропровод, газ', 'Двор': 'детская площадка, спортивная площадка',
              'Парковка': 'открытая во дворе', 'Количество комнат': '2', 'Общая площадь': '45.8 м²',
              'Площадь кухни': '7 м²',
              'Жилая площадь': '28.5 м²', 'Этаж': '4 из 9', 'Балкон или лоджия': 'лоджия',
              'Тип комнат': 'изолированные',
              'Высота потолков': '2.5 м', 'Санузел': 'раздельный', 'Окна': 'во двор', 'Ремонт': 'косметический',
              'Способ продажи': 'альтернативная', 'Вид сделки': 'возможна ипотека'},
             {'link': 'https://www.avito.ru/sankt-peterburg/kvartiry/2-k._kvartira_523m_618et._2443331462',
              'price': 8640000, 'address': 'Санкт-Петербург, Ленинский пр-т, 78к1', 'time': '22 06',
              'subway': 'Проспект Ветеранов', 'distance_to_subway': '3,8 км', 'Тип дома': 'панельный',
              'Год постройки': '2010', 'Этажей в доме': '18', 'Пассажирский лифт': '1', 'Грузовой лифт': '1',
              'Двор': 'детская площадка', 'Парковка': 'открытая во дворе', 'Количество комнат': '2',
              'Общая площадь': '52.3 м²', 'Площадь кухни': '8.6 м²', 'Жилая площадь': '32.2 м²', 'Этаж': '6 из 18',
              'Балкон или лоджия': 'лоджия', 'Тип комнат': 'изолированные', 'Высота потолков': '2.7 м',
              'Санузел': 'раздельный', 'Окна': 'на улицу, на солнечную сторону', 'Ремонт': 'требует ремонта',
              'Способ продажи': 'альтернативная', 'Вид сделки': 'возможна ипотека'},
             {'link': 'https://www.avito.ru/sankt-peterburg/kvartiry/2-k._kvartira_546m_12et._2375755329',
              'price': 8890000, 'address': 'Санкт-Петербург, пр-т Энгельса, 16', 'time': '22 06',
              'subway': 'Пионерская', 'distance_to_subway': '1,7 км', 'Тип дома': 'кирпичный', 'Год постройки': '1947',
              'Этажей в доме': '2', 'Пассажирский лифт': 'нет', 'Грузовой лифт': 'нет', 'Количество комнат': '2',
              'Общая площадь': '54.6 м²', 'Площадь кухни': '6.3 м²', 'Жилая площадь': '32.9 м²', 'Этаж': '1 из 2',
              'Тип комнат': 'смежные', 'Высота потолков': '2.8 м', 'Санузел': 'совмещенный', 'Окна': 'во двор',
              'Ремонт': 'косметический', 'Способ продажи': 'свободная'},
             {'link': 'https://www.avito.ru/sankt-peterburg/kvartiry/2-k._kvartira_46m_210et._2457583355',
              'price': 8300000, 'address': 'Санкт-Петербург, пр-т Авиаконструкторов, 15к1', 'time': '22 06',
              'subway': 'Комендантский проспект', 'distance_to_subway': '1 км', 'Тип дома': 'панельный',
              'Год постройки': '1987', 'Этажей в доме': '10', 'Пассажирский лифт': '1', 'Грузовой лифт': 'нет',
              'В доме': 'мусоропровод', 'Двор': 'детская площадка, спортивная площадка',
              'Парковка': 'открытая во дворе', 'Количество комнат': '2', 'Общая площадь': '46 м²',
              'Площадь кухни': '7 м²', 'Жилая площадь': '28 м²', 'Этаж': '2 из 10', 'Балкон или лоджия': 'лоджия',
              'Тип комнат': 'изолированные', 'Высота потолков': '2.6 м', 'Санузел': 'раздельный',
              'Окна': 'на улицу, на солнечную сторону', 'Ремонт': 'косметический',
              'Мебель': 'кухня, хранение одежды, спальные места', 'Техника': 'посудомоечная машина',
              'Способ продажи': 'свободная', 'Вид сделки': 'возможна ипотека'},
             {'link': 'https://www.avito.ru/sankt-peterburg/kvartiry/2-k._kvartira_407m_625et._2474334305',
              'price': 9500000, 'address': 'Санкт-Петербург, Выборгское ш., 17к3', 'time': '21 06',
              'subway': 'Проспект Просвещения', 'distance_to_subway': '1,2 км', 'Тип дома': 'монолитный',
              'Год постройки': '2008', 'Этажей в доме': '25', 'Пассажирский лифт': '2', 'Грузовой лифт': '2',
              'В доме': 'мусоропровод', 'Двор': 'детская площадка, спортивная площадка', 'Парковка': 'подземная',
              'Количество комнат': '2', 'Общая площадь': '40.7 м²', 'Площадь кухни': '12.7 м²',
              'Жилая площадь': '17 м²', 'Этаж': '6 из 25', 'Балкон или лоджия': 'балкон', 'Тип комнат': 'изолированные',
              'Высота потолков': '2.8 м', 'Санузел': 'совмещенный', 'Окна': 'во двор', 'Ремонт': 'евро',
              'Мебель': 'кухня', 'Способ продажи': 'альтернативная', 'Вид сделки': 'возможна ипотека'},
             {'link': 'https://www.avito.ru/sankt-peterburg/kvartiry/2-k._kvartira_451m_1112et._2473903964',
              'price': 9300000, 'address': 'Санкт-Петербург, Индустриальный пр-т, 15', 'time': '21 06',
              'subway': 'Ладожская', 'distance_to_subway': '2,4 км', 'Тип дома': 'панельный', 'Год постройки': '1987',
              'Этажей в доме': '12', 'Грузовой лифт': '1', 'В доме': 'мусоропровод',
              'Двор': 'детская площадка, спортивная площадка', 'Парковка': 'открытая во дворе',
              'Количество комнат': '2', 'Общая площадь': '45.1 м²', 'Площадь кухни': '7.2 м²', 'Жилая площадь': '26 м²',
              'Этаж': '11 из 12', 'Балкон или лоджия': 'лоджия', 'Тип комнат': 'изолированные',
              'Высота потолков': '2.7 м', 'Санузел': 'раздельный', 'Окна': 'на улицу, на солнечную сторону',
              'Ремонт': 'евро', 'Тёплый пол': 'есть', 'Мебель': 'кухня',
              'Техника': 'холодильник, стиральная машина, посудомоечная машина', 'Способ продажи': 'свободная',
              'Вид сделки': 'возможна ипотека'},
             {'link': 'https://www.avito.ru/sankt-peterburg/kvartiry/3-k._kvartira_572m_35et._2361812734',
              'price': 9190000, 'address': 'Санкт-Петербург, Благодатная ул., 35', 'time': '21 06',
              'subway': 'Электросила', 'distance_to_subway': '500 м', 'Тип дома': 'кирпичный', 'Этажей в доме': '5',
              'Пассажирский лифт': 'нет', 'Грузовой лифт': 'нет', 'В доме': 'газ',
              'Двор': 'детская площадка, спортивная площадка', 'Парковка': 'открытая во дворе',
              'Количество комнат': '3', 'Общая площадь': '57.2 м²', 'Площадь кухни': '6 м²', 'Жилая площадь': '40 м²',
              'Этаж': '3 из 5', 'Тип комнат': 'изолированные', 'Высота потолков': '2.6 м', 'Санузел': 'раздельный',
              'Окна': 'во двор, на улицу', 'Ремонт': 'косметический', 'Мебель': 'хранение одежды',
              'Способ продажи': 'свободная', 'Вид сделки': 'возможна ипотека'},
             {'link': 'https://www.avito.ru/sankt-peterburg/kvartiry/2-k._kvartira_51m_1625et._2393023407',
              'price': 5850000, 'address': 'Санкт-Петербург, Пушкинский р-н, пос. Шушары, Валдайская ул., 4к2',
              'time': '21 06', 'subway': 'Купчино', 'distance_to_subway': '3 км', 'Тип дома': 'монолитный',
              'Этажей в доме': '25', 'Количество комнат': '2', 'Общая площадь': '51 м²', 'Площадь кухни': '8.7 м²',
              'Жилая площадь': '29.5 м²', 'Этаж': '16 из 25', 'Балкон или лоджия': 'лоджия',
              'Тип комнат': 'изолированные', 'Санузел': 'раздельный', 'Окна': 'во двор, на улицу',
              'Ремонт': 'требует ремонта', 'Способ продажи': 'свободная'},
             {'link': 'https://www.avito.ru/sankt-peterburg/kvartiry/2-k._kvartira_565m_26et._2306068619',
              'price': 9400000, 'address': 'Санкт-Петербург, Опочинина ул., 9', 'time': '21 06', 'subway': 'Приморская',
              'distance_to_subway': '2,2 км', 'Тип дома': 'кирпичный', 'Год постройки': '1909', 'Этажей в доме': '6',
              'Пассажирский лифт': '1', 'В доме': 'газ', 'Парковка': 'открытая во дворе', 'Количество комнат': '2',
              'Общая площадь': '56.5 м²', 'Площадь кухни': '9.4 м²', 'Жилая площадь': '37.9 м²', 'Этаж': '2 из 6',
              'Тип комнат': 'изолированные', 'Высота потолков': '3.2 м', 'Санузел': 'совмещенный', 'Окна': 'во двор',
              'Ремонт': 'косметический', 'Способ продажи': 'свободная'},
             {'link': 'https://www.avito.ru/sankt-peterburg/kvartiry/2-k._kvartira_422m_15et._2466252380',
              'price': 5900000, 'address': 'Санкт-Петербург, Крюкова ул., 7', 'time': '21 06', 'subway': 'Ладожская',
              'distance_to_subway': '3,4 км', 'Тип дома': 'кирпичный', 'Год постройки': '1961', 'Этажей в доме': '5',
              'Двор': 'детская площадка, спортивная площадка', 'Парковка': 'открытая во дворе',
              'Количество комнат': '2', 'Общая площадь': '42.2 м²', 'Площадь кухни': '5.7 м²',
              'Жилая площадь': '27.2 м²', 'Этаж': '1 из 5', 'Тип комнат': 'изолированные', 'Высота потолков': '2.5 м',
              'Санузел': 'раздельный', 'Окна': 'во двор', 'Ремонт': 'требует ремонта', 'Способ продажи': 'свободная',
              'Вид сделки': 'возможна ипотека'},
             {'link': 'https://www.avito.ru/sankt-peterburg/kvartiry/2-k._kvartira_495m_712et._2447923406',
              'price': 9100000, 'address': 'Санкт-Петербург, ул. Латышских Стрелков, 11к2', 'time': '21 06',
              'subway': 'Проспект Большевиков', 'distance_to_subway': '1,1 км', 'Тип дома': 'панельный',
              'Год постройки': '1986', 'Этажей в доме': '12', 'Пассажирский лифт': '1', 'Грузовой лифт': '1',
              'Количество комнат': '2', 'Общая площадь': '49.5 м²', 'Площадь кухни': '7 м²', 'Жилая площадь': '31.2 м²',
              'Этаж': '7 из 12', 'Балкон или лоджия': 'балкон', 'Тип комнат': 'изолированные',
              'Высота потолков': '2.6 м', 'Санузел': 'раздельный', 'Окна': 'на улицу', 'Ремонт': 'косметический',
              'Мебель': 'кухня', 'Способ продажи': 'свободная', 'Вид сделки': 'возможна ипотека'}]


# class Parsed_cards(NamedTuple):
#     price: int

# create df
def _prepare_dataframe(raw_data_from_parser: list) -> pd.DataFrame:
    """This function create and prepare working dataframe with objects from parser"""
    cols = ['rating', 'time', 'price', 'address', 'subway', 'distance_to_subway', 'Количество комнат', 'Общая площадь',
            'Жилая площадь', 'Площадь кухни', 'Этаж', 'Балкон или лоджия', 'Ремонт', 'Вид сделки', 'Тип дома',
            'Запланирован снос', 'link']

    main_df = pd.DataFrame(columns=cols).append(raw_data_from_parser)[cols]
    # main_df = main_df.append(data_from_parser)[cols]
    # main_df = main_df[cols]
    main_df.columns = ['rating', 'time', 'price', 'address', 'subway', 'distance_to_subway', 'rooms', 'total_area', 'living_area',
                       'kitchen_area', 'floor', 'balcony', 'type_of_renovation', 'type_of_deal', 'type_of_house',
                       'demolition_plan', 'link']
    # main_df[main_df.select_dtypes(include=object).columns.to_list()] = main_df.select_dtypes(include=object).applymap(
    #     lambda x: np.nan if len(x) == 0 else x)

    return main_df


# Time prepare
def _time_changer(time):
    """This function converts time values and uses them in the _prepare_time func"""
    if time[0].lower() == 'вчера':
        yesterday = date.today() - timedelta(days=1)
        return yesterday.strftime('%Y-%m-%d')
    elif time[0].lower() == 'сегодня':
        yesterday = date.today() - timedelta(days=0)
        return yesterday.strftime('%Y-%m-%d')
    else:
        #return date.today().strftime('%Y-%m-%d')
        return time


def _prepare_time(df):
    """This function makes correct time column"""
    df['time'] = df['time'].apply(lambda x: _time_changer(x))
    return df['time']


# Subway / Distance to subway
def _prepare_subway(df):
    """Remove NaN-values from subway and distance_to_subway columns, and makes a correct distance column"""

    # Remove NaN
    df = df[~df['subway'].isna()].copy()
    df = df[~df['distance_to_subway'].isna()].copy()

    # Correct distance
    df['distance_to_subway'] = df['distance_to_subway'].apply(lambda x: x.strip().split()[0])
    df['distance_to_subway'] = df['distance_to_subway'].apply(
        lambda x: f'{x}00' if len(''.join(x.split(','))) < 3 else x)
    df['distance_to_subway'] = df['distance_to_subway'].str.replace(',', '').astype(int)

    return df[['subway', 'distance_to_subway']]


# Area
def _round_area(obj):
    first_value = int(obj.split()[0].split('.')[0])
    second_value = int(obj.split()[0].split('.')[-1])
    if second_value >= 5:
        return first_value + 1
    else:
        return first_value


def _prepare_area(df):
    df['total_area'] = df['total_area'].apply(lambda x: x.split()[0].split('.')[0])
    df['kitchen_area'] = df['kitchen_area'].apply(
        lambda x: int(x.split()[0].split('.')[0]) + 1 if int(x.split()[0].split('.')[-1]) >= 5 else int(
            x.split()[0].split('.')[0]))
    df['living_area'] = df['living_area'].apply(lambda x: _round_area(x) if pd.notnull(x) else x)
    return df[['total_area', 'kitchen_area', 'living_area']]


def _prepare_floors(df):
    df['floor'] = df['floor'].apply(lambda x: x.split())
    df['cur_floor'] = df['floor'].apply(lambda x: x[0])
    df['cnt_floors'] = df['floor'] = df['floor'].apply(lambda x: x[-1])
    return df


def _drop_columns(df):
    df = df.loc[df['demolition_plan'] != 'да'].copy()
    df = df[(df['type_of_deal']).isna() | (df['type_of_deal'] == "возможна ипотека")].copy()
    df = df[df['cnt_floors'] != '1'].copy()
    df = df.loc[df['cnt_floors'] != df['cur_floor']].copy()

    df = df.drop('demolition_plan', axis=1)
    df = df.drop('type_of_deal', axis=1)
    df = df.drop('floor', axis=1)

    return df


def _fill_nan(df):
    df.loc[df['type_of_renovation'].isna(), 'type_of_renovation'] = 'неизвестно'
    df.loc[df['balcony'].isna(), 'balcony'] = 'нет'
    return df


def prepare_parsed_card(raw_data: list) -> pd.DataFrame:
    """Prepare clean dataframe after raw parser
    :param raw_data: raw list of dictionaries after parsing
    :return: Updated Dataframe
    """
    imputer = KNNImputer(n_neighbors=3)

    print('Создали дф')
    df = _prepare_dataframe(raw_data)
    print('тайм')
    df['time'] = _prepare_time(df)
    print('сабвей')
    df[['subway', 'distance_to_subway']] = _prepare_subway(df)
    print('ареа')
    df[['total_area', 'kitchen_area', 'living_area']] = _prepare_area(df)
    print('импьютер')
    df[['total_area', 'living_area', 'kitchen_area']] = imputer.fit_transform(
        df[['total_area', 'living_area', 'kitchen_area']])
    # df.to_csv(r'C:\Users\q\Desktop\view.csv', encoding='utf-8-sig')
    print('обнулить отступы')
    # df[df.select_dtypes(include=object).columns.to_list()] = df.select_dtypes(include=object).applymap(
    #    lambda x: x.strip() if pd.notnull(x) else x)
    # print(df)
    print('этажи')
    df = _prepare_floors(df)
    print('drop')
    df = _drop_columns(df)
    print('fillna')
    df = _fill_nan(df)

    return df


if __name__ == "__main__":
    ddd = prepare_parsed_card(data_test)
    print(ddd)
    ddd.to_csv(r'C:\Users\q\Desktop\view.csv', index=False)

    # посмотрим какие тут данные
    # и к каждому df['column'] применим функцию _четототам
