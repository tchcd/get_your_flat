from avito_parser_class import AvitoParser
import logging
from src.logcfg import logger_cfg
from transform_data import DataTransformation, SaveToJson, SaveToCsv
from src.database import Database
from src import exceptions
import cfg

logging.config.dictConfig(logger_cfg)
log_error = logging.getLogger('log_error')
log_info = logging.getLogger('log_info')


def avito_etl(database):
    """Pipeline avito parsing -> prepare raw data -> add prepared data to database"""
    try:
        log_info.info("PARSING HAS BEEN STARTED")
        data = AvitoParser(headless=True).start_parser(count_url=cfg.URL_COUNT)
        log_info.info("PARSING HAS BEEN SUCCESSFULLY COMPLETED")
        SaveToJson(data).save()

        log_info.info("DATA PREPARING HAS BEEN STARTED")
        transformed_df = DataTransformation().start_transform(data)
        log_info.info("PARSED DATA HAS BEEN SUCCESSFULLY PREPARED")
        SaveToCsv(transformed_df).save()

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

