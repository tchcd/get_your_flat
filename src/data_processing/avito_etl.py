from avito_parser_class import AvitoParser
import logging
from src.logcfg import logger_cfg
from transform_data import DataHandler, JsonWriter, CsvWriter
from src.database import Database
from src import exceptions as exc
import cfg

logging.config.dictConfig(logger_cfg)
logger = logging.getLogger('logger')


def avito_etl(database: Database) -> None:
    """Pipeline avito parsing -> transform raw data -> add prepared data to database"""
    try:
        logger.info("PARSING HAS BEEN STARTED")
        data = AvitoParser(headless=cfg.SELENIUM_HEADLESS).start_parser(count_url=cfg.PAGES_TO_PARSE_NUM)
        logger.info("PARSING HAS BEEN SUCCESSFULLY COMPLETED")
        JsonWriter(data).save()

        logger.info("DATA PREPARING HAS BEEN STARTED")
        transformed_df = DataHandler().start_transform(data)
        logger.info("PARSED DATA HAS BEEN SUCCESSFULLY PREPARED")
        CsvWriter(transformed_df).save()

        database.insert_flat(column_values=transformed_df)
        logger.info(f"{len(transformed_df)} ITEMS HAS BEEN ADDED TO DATABASE")

    except exc.ParsingNotComplete:
        raise
    except exc.TransformDataNotComplete:
        raise
    except exc.AddToDBFailed:
        raise
    except exc.DBConnectionFailed:
        raise


if __name__ == "__main__":
    db = Database()
    avito_etl(db)

