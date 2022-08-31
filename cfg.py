import os
from pathlib import Path
from datetime import datetime

DATE_NOW = datetime.now().date().strftime(format='%m-%d')

# Paths
MAIN_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Database path
PATH_TO_DB = Path(MAIN_FOLDER) / 'flats.db'

# Data paths
RAW_DATA_PATH_JSON = Path(f"{MAIN_FOLDER}/files/process") / f"raw_data_{DATE_NOW}.json"
TRANSFORMED_DATA_PATH_CSV = Path(f"{MAIN_FOLDER}/files/process") / f"transformed_data_{DATE_NOW}.csv"

# Models paths
MODELS_PATH = os.path.join(MAIN_FOLDER, 'models')
PATH_TO_SAVE_MODEL = Path(MODELS_PATH) / 'cb_last.sav'
PATH_TO_LAST_MODEL = Path(MODELS_PATH) / 'cb_last.sav'
PATH_TO_INIT_MODEL = Path(MODELS_PATH) / 'cb_init.sav'

# Logger paths
ERRORS_LOG_FILE = Path(f"{MAIN_FOLDER}/logs") / 'errors.log'
INFO_LOG_FILE = Path(f"{MAIN_FOLDER}/logs") / 'info.log'

# Parser parameters
URL_COUNT = 20
SELENIUM_HEADLESS = True

# ML model parameters
MODEL_PARAMS = {
    'learning_rate': 0.05,
    'iterations': 5000,
    'early_stopping_rounds': 500
}

# Columns for predict and retrain ML model
COLUMNS = ['rating', 'price', 'sqmeter_price', 'subway', 'minutes_to_subway', 'rooms', 'total_area',
           'balcony', 'type_of_renovation', 'type_of_house', 'cur_floor', 'cnt_floors']

if __name__ == '__main__':
    print(RAW_DATA_PATH_JSON)
    pass