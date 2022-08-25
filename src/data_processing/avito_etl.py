from avito_parser_daily_script import avito_parse_start
from avito_parser_class import AvitoParser
from datetime import datetime
import logging
from src.logcfg import logger_cfg
from transform_data import DataTransformation, SaveJson, SaveCsv
from src.database import Database
from src import exceptions

logging.config.dictConfig(logger_cfg)
log_error = logging.getLogger('log_error')
log_info = logging.getLogger('log_info')


def avito_etl(database):
    """Pipline avito parsing -> prepare raw data -> add prepared data to database"""
    try:
        log_info.info("PARSING HAS BEEN STARTED")
        data = AvitoParser(headless=True).run_parser(count_url=15)
        log_info.info("PARSING HAS BEEN SUCCESSFULLY COMPLETED")
        SaveJson.save(data)

        log_info.info("DATA PREPARING HAS BEEN STARTED")
        transformed_df = DataTransformation.start_preparing(data)
        log_info.info("PARSED DATA HAS BEEN SUCCESSFULLY PREPARED")
        SaveCsv.save(transformed_df)

        database.add_parsed_items(column_values=transformed_df)
        log_info.info(f"{len(transformed_df)} ITEMS HAS BEEN ADDED TO DATABASE")

    except exceptions.prepare_data_failed as err:
        log_error.exception(err)
    except exceptions.parse_data_failed as err:
        log_error.exception(err)
    except exceptions.db_connect_failed as err:
        log_error.error('NOT CONNECTED TO DATABASE')
        log_error.exception(err)


if __name__ == "__main__":
    db = Database()
    avito_etl(db)

