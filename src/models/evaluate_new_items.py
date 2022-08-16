import pickle
import pandas as pd
from src.database import Database
from src import exceptions
import os
import logging
from src.logcfg import logger_cfg

logging.config.dictConfig(logger_cfg)
log_error = logging.getLogger('log_error')
log_info = logging.getLogger('log_info')

PATH_TO_LAST_MODEL = '../../models/cb_last.sav'

if os.path.exists(PATH_TO_LAST_MODEL):
    MODEL_PATH = PATH_TO_LAST_MODEL
else:
    MODEL_PATH = PATH_TO_LAST_MODEL

MODEL = pickle.load(open(MODEL_PATH, "rb"))
COLUMNS = MODEL.feature_names_


def get_daily_predict(model) -> pd.DataFrame:                   # This func need to refactor
    """
    Predict not evaluated items after parsing function.
    Get not estimated items from db -> predict rating for them -> update rating in db.
    """
    try:
        db = Database()
        df = db.get_not_estimated_items()
        df["rating"] = model.predict(df[COLUMNS])
        db.update_estimated_items(df)
        log_info.info(f'{df.shape[0]} NEW ITEMS HAS BEEN EVALUATED')
    except:
        log_error.error('WORK PREDICTION MODEL HAS BEEN FAILED')
        raise exceptions.evaluate_data_failed

    return df


if __name__ == "__main__":
    get_daily_predict(MODEL)

# Проблема в том, что переобученая модель предсказывает только итемы с НаН, в том числе из за апдейта БД где rating is Null