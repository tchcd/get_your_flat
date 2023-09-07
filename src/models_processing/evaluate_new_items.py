import pickle
import pandas as pd
from src.database import Database
import src.exceptions as exc
import os
import logging
from src.logcfg import logger_cfg
from cfg import PATH_TO_INIT_MODEL, PATH_TO_LAST_MODEL

logging.config.dictConfig(logger_cfg)
logger = logging.getLogger('logger')

if os.path.exists(PATH_TO_LAST_MODEL):
    MODEL_PATH = PATH_TO_LAST_MODEL
    logger.info(f'LAST MODEL SELECTED')
else:
    MODEL_PATH = PATH_TO_INIT_MODEL
    logger.info(f'INIT MODEL SELECTED')

MODEL = pickle.load(open(MODEL_PATH, "rb"))
COLUMNS = MODEL.feature_names_


def predict_new_flats_rating(model, database: Database) -> pd.DataFrame:
    """
    Predict not evaluated items after parsing function.
    Get not estimated items from db -> predict rating for them -> update rating in db.
    """
    try:
        df = database.get_not_estimated_items()
        if len(df) == 0:
            raise exc.NotItemsWithoutRating
        df["rating"] = model.predict(df[COLUMNS])
        database.update_flat_rating(df)
    except exc.DBConnectionFailed:
        raise
    except exc.NotItemsWithoutRating:
        raise
    except exc.UpdateDBItemsFailed:
        raise
    else:
        logger.info(f'{df.shape[0]} NEW ITEMS HAS BEEN EVALUATED')
        return df


if __name__ == "__main__":
    db = Database()
    predict_new_flats_rating(MODEL, db)
