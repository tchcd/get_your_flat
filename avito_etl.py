import pandas as pd
from avito_parser_daily_script import avito_parse_start
from prepare_data import prepare_parsed_card, get_not_duplicated_items
from database import Database
import exceptions
import json


# 1 этаж убить из модели
# очень большой вес дать станциям метро и внимательно их отследить, киллер фича

def avito_etl():  # -> собственный namedtuple
    try:
        db = Database()
        db.setup()  # already created
    except exceptions.db_connect_fail as err:
        print(err)
        # logger.error(error)
        raise

    # Start daily parser
    try:
        data = avito_parse_start(headless=False)
    except:
        print('parser does not work')

    try:
        with open('raw_parsed_items1.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f'raw json was not written {e}')

    # Start prepare raw cards
    try:
        prepared_df = prepare_parsed_card(data)
        not_duplicated_items = get_not_duplicated_items(df=prepared_df, db_name=db)
    except Exception as err:
        # logger.error(err)
        print(f'prepared df was not written', err)
    finally:
        prepared_df.to_json('prepared_items_df1.json', force_ascii=False, indent=4)
        prepared_df.to_csv(r'C:\Users\q\Desktop\view.csv', index=False)

    # DB module
    try:
        db.add_parsed_items(column_values=not_duplicated_items)
    except exceptions.db_connect_fail as e:
        print(f'{e} error database')


if __name__ == "__main__":
    avito_etl()
