from src.models.catboost_estimation_model import get_daily_predict
from datetime import datetime
DATE_NOW = datetime.now().date().strftime(format='%m-%d')


def prediction_new_items():
    estimation_df = get_daily_predict()
    estimation_df.to_csv(f"../../files/process/estimated_df_{DATE_NOW}.csv")


if __name__ == "__main__":
    prediction_new_items()
