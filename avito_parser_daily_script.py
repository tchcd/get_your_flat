# Это парсер для ежедневных (сегодня) объявлений именно скрипт
# Вся логика в avito_parser

from avito_parser_class import AvitoParser


# 1. start_daily_parse - активирует парсинг, на выходе отдает словарь? объявлений
# 2. prepare_parsed_card, которая обрабатывает спаршенные объявления, делает их окей
# 3. to_sql - функция, которая принимает prepare_parsed_card и льет их в БД


def avito_parse(headless=False) -> list:
    if headless:
        parser = AvitoParser(headless=True)
    else:
        parser = AvitoParser()
    parser.auth_avito()
    parser.get_filters()
    pages = parser.pages_generation()
    parser.parse_objects(pages)
    return parser.storage


# print(storage)

# Тестовая функция db insert

# Database.add_items('flat_db', {
#     'column_1': 'data',
#     'column_2': 'data2',
#     'columns_3': 'Тут может быть любая функция из prepare_data'
# })

if __name__ == "__main__":
    storage = avito_parse()
    print(storage)
