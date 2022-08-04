from src.database import Database
from src.models.catboost_estimation_model import get_daily_predict



def prediction_new_items():
    db = Database()
    estimation_df = get_daily_predict()
    estimation_df.to_csv(f"../../files/process/estimated_df_{1}.csv")
    #db.replace_estimated_cards(estimation_df)
    print(estimation_df)


if __name__ == "__main__":
    prediction_new_items()
