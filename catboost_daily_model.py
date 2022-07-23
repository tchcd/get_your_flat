import pickle
import json
import pandas as pd

# Для начала нужно из jupyter выгрузить обученную модель кэтбуст
# и подгружаем здесь


last_model_path = r"C:\Users\q\PycharmProjects\Flat_bot\models\init_model.sav"
model = pickle.load(open(last_model_path, "rb"))
cols = model.feature_names_


# Здесь функция кэтбуста
def get_daily_predict(raw_json: json) -> pd.DataFrame:
    """CatBoost function does predictions for not evaluation dataframe after parsing function

    Args:
        raw_json (json) : json with data objects

    Returns:
        pd.DataFrame: with evaluation value. Sending to the database

    """

    df = pd.read_json(raw_json)
    df["rating"] = model.predict(df[cols])
    return df


if __name__ == "__main__":
    predict = get_daily_predict("json_prep.json")
    predict.to_csv(r"C:\Users\q\Desktop\view_w_r.csv")
