import pickle
import json
import pandas as pd
from src.database import Database
from datetime import datetime


BASE_MODEL_PATH = "../../models/cb_init.sav"
LAST_MODEL_PATH = "../../models/cb_last.sav"
MODEL = pickle.load(open(LAST_MODEL_PATH, "rb"))
COLUMNS = MODEL.feature_names_


def get_daily_predict() -> pd.DataFrame:
    """CatBoost function does predictions for not evaluation dataframe after parsing function
    Args:
        raw_json (json) : json with data objects
    Returns:
        pd.DataFrame: with evaluation value. Sending to the database
    """
    db = Database()
    df = db.get_all_items()
    df["rating"] = MODEL.predict(df[COLUMNS])
    return df


if __name__ == "__main__":
    estimation_df = get_daily_predict()
    estimation_df.to_csv(f"../../files/process/estimated_df_{1}.csv")
    print('gotovo')


