# Логика, склейка
from avito_parser_daily_script import avito_parse
from prepare_data import prepare_parsed_card
from database import Database
from prepare_data import data_test
import json


#ДОБАВИТЬ SHOWN COLUMN
#1 этаж убить из модели
#очень большой вес дать станциям метро и внимательно их отследить, киллер фича

# Подготовщик данных
# отправляем в SQL

# Вызываем ежедневный парсер

def avito_etl():  # -> собственный namedtuple
    # Parser module
    try:
        data = avito_parse(headless=True)
    except:
        print('parser does not work')
    try:
        with open('parse_1.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except:
        print('not jsoning')
    # Prepare module
    try:
        prepared_df = prepare_parsed_card(data)
    except:
        print('prepare does not work')

    try:
        prepared_df.to_json('json_prep.json', force_ascii=False, indent=4)
    except:
        print('not jsoning prep')
    finally:
        prepared_df.to_csv(r'C:\Users\q\Desktop\view.csv', index=False)


# new_parsed_cards = start_daily_parse()


# Вызываем функцию подготовки данных из модуля prepare_data
# good_new_cards = prepare_parsed_card(new_parsed_cards: Parsed_cards) #-> а отдаем либо df либо json
# для функции обработки

# Отправляем SQL в DB
# Database.add_daily_avito_cards_to_db(good_new_cards) #принимает json отдает ?? в БД

if __name__ == "__main__":
    avito_etl()
    # its_json = js()
    # prepared_df = prepare_parsed_card(its_json)
