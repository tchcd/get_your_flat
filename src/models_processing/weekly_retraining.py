from catboost import CatBoostRegressor
from datetime import datetime
import logging
import pickle
from sklearn.model_selection import train_test_split
from src.database import Database
from src.logcfg import logger_cfg
from src import exceptions

logging.config.dictConfig(logger_cfg)
log_error = logging.getLogger('log_error')
log_info = logging.getLogger('log_info')
DATE_NOW = datetime.now().date().strftime(format='%m-%d')
COLUMNS = ['rating', 'price', 'sqmeter_price', 'subway', 'minutes_to_subway', 'rooms', 'total_area',
           'balcony', 'type_of_renovation', 'type_of_house', 'cur_floor', 'cnt_floors']

def evaluation(df):
    cnt = 0

    # price
    const = 1000000
    cnt += (10 - df['price'] / const) * 0.1  # 0.1 or 0.15 coef

    # subways
    one = ['Девяткино', 'Звёздная', 'Комендантский проспект', 'Купчино', 'Парнас',
           'Проспект Большевиков', 'Рыбацкое', 'Улица Дыбенко', 'Проспект Славы',
           'Дунайская', 'Шушары', 'Проспект Ветеранов']
    two = ['Академическая', 'Гражданский проспект', 'Ленинский проспект',
           'Международная', 'Бухарестская', 'Ладожская', 'Новочеркасская',
           'Площадь Мужества', 'Обухово', 'Политехническая', 'Проспект Просвещения',
           'Удельная']
    three = ['Автово', 'Выборгская', 'Нарвская', 'Кировский завод', 'Пионерская',
             'Пролетарская', 'Чёрная речка', 'Чернышевская', 'Чкаловская']
    four = ['Волковская', 'Звенигородская', 'Крестовский остров', 'Лесная',
            'Московская', 'Московские ворота', 'Озерки', 'Парк Победы',
            'Приморская', 'Спортивная', 'Электросила']
    five = ['Горьковская', 'Гостиный двор', 'Адмиралтейская', 'Балтийская',
            'Василеостровская', 'Владимирская', 'Достоевская', 'Елизаровская',
            'Лиговский проспект', 'Ломоносовская', 'Маяковская', 'Невский проспект',
            'Обводный канал', 'Петроградская', 'Площадь А. Невского I',
            'Площадь А. Невского II', 'Площадь Восстания', 'Площадь Ленина',
            'Пушкинская', 'Садовая', 'Сенная площадь', 'Спасская', 'Старая Деревня',
            'Технологический ин-т II', 'Технологический ин-т I', 'Фрунзенская',
            'Василеостровская']

    if df['subway'] in one:
        cnt += 0.1
    elif df['subway'] in two:
        cnt += 0.2
    elif df['subway'] in three:
        cnt += 0.3
    elif df['subway'] in four:
        cnt += 0.4
    elif df['subway'] in five:
        cnt += 0.5
    else:
        cnt += 0.25

    # distance_to_subway
    if df['minutes_to_subway'] <= 5:
        cnt += 0.3
    elif df['minutes_to_subway'] <= 10:
        cnt += 0.4
    elif df['minutes_to_subway'] <= 15:
        cnt += 0.35
    elif df['minutes_to_subway'] <= 20:
        cnt += 0.2
    elif df['minutes_to_subway'] <= 30:
        cnt += 0.1
    elif df['minutes_to_subway'] > 30:
        cnt += 0
    else:
        cnt += 0.3

    # Floor
    if df['cur_floor'] < 2:
        cnt += 0
    elif df['cur_floor'] == 2:
        cnt += 0.3
    elif df['cur_floor'] <= 3:
        cnt += 0.4
    elif df['cur_floor'] <= 5:
        cnt += 0.25
    elif df['cur_floor'] <= 8:
        cnt += 0.1
    elif df['cur_floor'] <= 10:
        cnt += 0.05
    elif df['cur_floor'] <= 15:
        cnt += 0
    elif df['cur_floor'] > 15:
        cnt += 0
    else:
        cnt += 0.1

    # balcony
    if df['balcony'] == 'нет':
        cnt += 0.05
    elif df['balcony'] == 'балкон':
        cnt += 0.25
    elif df['balcony'] == 'лоджия':
        cnt += 0.3
    elif df['balcony'] == 'балкон, лоджия':
        cnt += 0.25
    else:
        cnt += 0.1

    # type_of_hose
    if df['type_of_house'] == 'кирпичный':
        cnt += 0.35
    elif df['type_of_house'] == 'панельный':
        cnt += 0.2
    elif df['type_of_house'] == 'блочный':
        cnt += 0.25
    elif df['type_of_house'] == 'монолитный':
        cnt += 0.1
    elif df['type_of_house'] == 'монолитно-кирпичный':
        cnt += 0.35
    else:
        cnt += 0.15

    # renovation
    if df['type_of_renovation'] == 'косметический':
        cnt += 0.25
    elif df['type_of_renovation'] == 'требует ремонта':
        cnt += 0.1
    elif df['type_of_renovation'] == 'евро':
        cnt += 0.4
    elif df['type_of_renovation'] == 'дизайнерский':
        cnt += 0.4
    elif df['type_of_renovation'] == 'неизвестно':
        cnt += 0.1
    else:
        cnt += 0.1

    # rooms
    if df['rooms'] == 2:
        cnt += 0.3
    if df['rooms'] == 3:
        cnt += 0.45

    return round(cnt * 100)


def prepare_training_dataset(df):
    try:
        df = df[COLUMNS].copy()
        X = df.drop('rating', axis=1)
        y = df['rating']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=20)
        cat_features = [X_train.columns.get_loc(col) for col in X_train.select_dtypes(include=object).columns]
    except:
        raise exceptions.prepare_model_failed

    return X_train, X_test, y_train, y_test, cat_features


def save_model(model, output_path):
    pickle.dump(model, open(output_path, 'wb'))


def weekly_retraining_model():
    db = Database()
    all_items = db.get_all_items()

    try:
        all_items['rating'] = all_items.apply(evaluation, axis=1)
        log_info.info("EQUATION HAS BEEN APPLIED")
    except:
        log_error.error('EQUATION HAS NOT BEEN APPLIED!')
        raise exceptions.prepare_model_failed


    try:
        X_train, X_test, y_train, y_test, cat_features = prepare_training_dataset(all_items)
        log_info.info("TRAIN/TEST HAS BEEN APPLIED")
    except:
        log_error.error('TRAIN/TEST HAS NOT BEEN SPLIT!')
        raise exceptions.prepare_model_failed

    try:
        model = CatBoostRegressor(learning_rate=0.05, iterations=5000, early_stopping_rounds=200)
        model.fit(X_train, y_train, eval_set=(X_test, y_test), cat_features=cat_features)
        save_model(model, "../../models/cb_last.sav")
        save_model(model, f"../../models/cb_last{DATE_NOW}_backup.sav")    # Здесь MLflow сохраняет бекап и параметры

        log_info.info("MODEL HAS BEEN TRAINED AND SAVED")
        # print(X_train.columns)
        # print(cat_features)

    except:
        log_error.error('MODEL HAS NOT BEEN TRAINED!')
        raise exceptions.prepare_model_failed


if __name__ == "__main__":
    weekly_retraining_model()



