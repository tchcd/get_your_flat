import pickle
import pandas as pd
from src.database import Database
from src import exceptions
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


def get_daily_predict(model, db) -> pd.DataFrame:
    """
    Predict not evaluated items after parsing function.
    Get not estimated items from db -> predict rating for them -> update rating in db.
    """
    try:
        df = db.get_not_estimated_items()
        df["rating"] = model.predict(df[COLUMNS])
        db.update_estimated_items(df)
    except Exception as err:
        logger.error('WORK PREDICTION MODEL HAS BEEN FAILED', err, exc_info=True)
        raise
    else:
        logger.info(f'{df.shape[0]} NEW ITEMS HAS BEEN EVALUATED')
        return df


if __name__ == "__main__":
    db = Database()
    get_daily_predict(MODEL, db)

# Проблема в том, что переобученая модель предсказывает только итемы с НаН, в том числе из за апдейта БД где rating is Null