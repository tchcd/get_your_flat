# Логика, склейка
import pandas as pd
from avito_parser_daily_script import avito_parse
from prepare_data import prepare_parsed_card, get_not_duplicated_items
#from test import get_not_duplicated_items
from database import Database
from test import data_test
import exceptions
import json


# ДОБАВИТЬ SHOWN COLUMN
# 1 этаж убить из модели
# очень большой вес дать станциям метро и внимательно их отследить, киллер фича

# Подготовщик данных
# отправляем в SQL

# Вызываем ежедневный парсер




def avito_etl():  # -> собственный namedtuple
    try:
        db = Database()
        db.setup()  # already created
    except:
        raise exceptions.db_connect_fail

    # Parser module
    # try:
    #    data = avito_parse(headless=True)
    # except:
    #    print('parser does not work')

    # try:
    #    with open('raw_parsed_items.json', 'w', encoding='utf-8') as file:
    #        json.dump(data, file, indent=4, ensure_ascii=False)
    # except exceptions.file_write_fail as e:
    #    print(f'raw json was not written {e}')

    # Prepare module
    # try:
    #    prepared_df = prepare_parsed_card(data)
    # except exceptions.file_write_fail as e:
    #    print(f'prepared df was not written {e}')

    # try:
    #    prepared_df.to_json('prepared_items_df.json', force_ascii=False, indent=4)
    # except:
    #    print('not jsoning prep')
    # finally:
    #    prepared_df.to_csv(r'C:\Users\q\Desktop\view.csv', index=False)

    ###### TEST ######

    # Prepare module
    try:
        prepared_df = prepare_parsed_card(data_test)
        prepared = get_not_duplicated_items(df=prepared_df, db_name=db)
    except:
        print(f'prepared df was not written')
        raise exceptions.file_write_fail

    try:
        db.add_parsed_items(column_values=prepared)
    except exceptions.db_connect_fail as e:
        print(f'{e} error database')



# Отправляем SQL в DB
# Database.add_daily_avito_cards_to_db(good_new_cards) #принимает json отдает ?? в БД

if __name__ == "__main__":
    avito_etl()
    # its_json = js()
    # prepared_df = prepare_parsed_card(its_json)
