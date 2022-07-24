# Это парсер для ежедневных (сегодня) объявлений именно скрипт
# Вся логика в avito_parser
import exceptions
from avito_parser_class import AvitoParser


# 1. start_daily_parse - активирует парсинг, на выходе отдает словарь? объявлений
# 2. prepare_parsed_card, которая обрабатывает спаршенные объявления, делает их окей
# 3. to_sql - функция, которая принимает prepare_parsed_card и льет их в БД


def avito_parse_start(headless=False) -> list:
    if headless:
        parser = AvitoParser(headless=True)
    else:
        parser = AvitoParser()
    try:
        parser.auth_avito()
        parser.get_filters()
        pages = parser.pages_generation()
        parser.parse_objects(pages)
    except:
        raise exceptions.parse_data_failed

    return parser.storage


if __name__ == "__main__":
    pass
