import logging

import pandas as pd

from src.logcfg import logger_cfg
from datetime import datetime
from avito_parser_daily_script import avito_parse_start
from prepare_data import prepare_parsed_card, get_not_duplicated_items
from src.database import Database
import src.database
from src import exceptions
import json
import os

logging.config.dictConfig(logger_cfg)
log_error = logging.getLogger('log_error')
log_info = logging.getLogger('log_info')
DATE_NOW = datetime.now().date().strftime(format='%m-%d')

def avito_etl():
    """Pipline avito parsing -> prepare raw data -> add prepared data to database"""
    try:
        db = Database()
        db.setup()  # already created
    except exceptions.db_connect_failed as err:
        log_error.error('NOT CONNECTED TO DATABASE')
        log_error.exception(err)

    # # Start daily parsing
    try:
        log_info.info("PARSING HAS STARTED")
        data = avito_parse_start(headless=True)
        log_info.info("PARSING HAS BEEN SUCCESSFULLY COMPLETED")
    except exceptions.parse_data_failed as err:
        log_error.exception(err)
    finally:
        with open(f"../../files/process/raw_parsed_items_{DATE_NOW}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


    # Start preparing raw cards
    try:
        log_info.info("DATA PREPARING HAS STARTED")
        prepared_df = prepare_parsed_card(data)
        log_info.info("PARSED DATA HAS BEEN SUCCESSFULLY PREPARED")
    except exceptions.prepare_data_failed as err:
        log_error.exception(err)
    finally:
        pass
        prepared_df.to_json(f"../../files/process/prepared_items_df_{DATE_NOW}.json", force_ascii=False, indent=4)
        prepared_df.to_csv(f"../../files/process/prepared_items_df_{DATE_NOW}.csv", index=False, encoding='utf-8-sig')

    # Add parsed items to database and delete duplicates
    try:
        not_duplicated_items = get_not_duplicated_items(df=prepared_df, db_name=db)
        db.add_parsed_items(column_values=not_duplicated_items)
        log_info.info('PREPARED DATA ADDED TO DATABASE')
    except exceptions.db_data_transfer_failed as err:
        log_error.exception(err)


if __name__ == "__main__":
    avito_etl()

