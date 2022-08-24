from avito_parser_daily_script import avito_parse_start
from avito_parser_class import AvitoParser
from datetime import datetime
import logging
from src.logcfg import logger_cfg
from prepare_data import prepare_parsed_card, get_not_duplicated_items
from src.database import Database
from src import exceptions
import json
import os

logging.config.dictConfig(logger_cfg)
log_error = logging.getLogger('log_error')
log_info = logging.getLogger('log_info')
DATE_NOW = datetime.now().date().strftime(format='%m-%d')


def avito_etl(db):
    """Pipline avito parsing -> prepare raw data -> add prepared data to database"""
    try:

        db.setup()  # already created
    except exceptions.db_connect_failed as err:
        log_error.error('NOT CONNECTED TO DATABASE')
        log_error.exception(err)

    # # Start daily parsing
    try:
        log_info.info("PARSING HAS STARTED")
        data = AvitoParser(headless=True).run_parser(count_url=15)
        log_info.info("PARSING HAS BEEN SUCCESSFULLY COMPLETED")

    # finally:
    #     with open(f"../../files/process/raw_parsed_items_{DATE_NOW}.json", "w", encoding="utf-8") as file:
    #         json.dump(data, file, indent=4, ensure_ascii=False)

    # Start preparing raw cards
    #try:
        log_info.info("DATA PREPARING HAS STARTED")
        prepared_df = prepare_parsed_card(data)
        to csv
        log_info.info("PARSED DATA HAS BEEN SUCCESSFULLY PREPARED")
    except exceptions.prepare_data_failed as err:
        log_error.exception(err)
    except exceptions.parse_data_failed as err:
        log_error.exception(err)
    # finally:
    #     prepared_df.to_json(f"../../files/process/prepared_items_df_{DATE_NOW}.json", force_ascii=False, indent=4)
    #     prepared_df.to_csv(f"../../files/process/prepared_items_df_{DATE_NOW}.csv", index=False, encoding='utf-8-sig')

    # Add parsed items to database and check if items exists in db

    db.add_parsed_items(column_values=not_duplicated_items)

    #
    # try:
    #     not_duplicated_items = get_not_duplicated_items(df=prepared_df, db_name=db)
    #
    #     log_info.info(f'{len(not_duplicated_items)} ITEMS HAVE BEEN ADDED TO DATABASE')
    # except exceptions.db_data_transfer_failed as err:
    #     log_error.exception(err)


if __name__ == "__main__":
    db = Database()
    avito_etl()

