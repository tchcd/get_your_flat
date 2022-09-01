import pandas as pd
import mlflow
from catboost import CatBoostRegressor
import logging
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from src.database import Database
from src.logcfg import logger_cfg
import cfg
import src.exceptions as exc

logging.config.dictConfig(logger_cfg)
logger = logging.getLogger('logger')


class ModelRetraining:
    def __init__(self, database: Database, save_path: str):
        self.db = database
        self.save_path = save_path

    @staticmethod
    def _get_target(df: pd.DataFrame) -> int:
        """Estimates each item by the expression"""
        cnt = 0

        try:
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

        except Exception as err:
            raise exc.RatingEquationFailed from err
        else:
            return round(cnt * 100)

    @staticmethod
    def _prepare_training_dataset(df: pd.DataFrame):
        try:
            df = df[cfg.COLUMNS].copy()
            X = df.drop('rating', axis=1)
            y = df['rating']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.4, random_state=42)
            cat_features = [X_train.columns.get_loc(col) for col in X_train.select_dtypes(include=object).columns]
            return X_train, X_val, X_test, y_train, y_val, y_test, cat_features
        except Exception as err:
            raise exc.TrainTestSplitFailed from err

    @staticmethod
    def _get_model_score(y_true, y_pred):
        """Evaluate quality of the retrained model
        :return: two metrics -> MAE and MAPE
        """
        try:
            mae = mean_absolute_error(y_true, y_pred)
            mape = mean_absolute_percentage_error(y_true, y_pred)
        except Exception as err:
            raise exc.EstimateModelFailed from err
        else:
            return mae, mape

    @staticmethod
    def _save_model(model, output_path):
        pickle.dump(model, open(output_path, 'wb'))

    def start_model_retraining(self):
        """
        Get all items from database -> get train/test dfs -> retrain and save model
        :return: two metrics MAE and MAPE
        """

        try:
            all_items_df = db.get_all_items()
            if len(all_items_df) == 0:
                raise exc.NotItemsWithoutRating

            all_items_df['rating'] = all_items_df.apply(self._get_target, axis=1)
            logger.info("RATING EQUATION HAS BEEN APPLIED")

            X_train, X_val, X_test, y_train, y_val, y_test, cat_features = self._prepare_training_dataset(all_items_df)
            logger.info("TRAIN/TEST HAS BEEN SPLIT")

            # Retraining model with MLFlow tracking
            mlflow.set_tracking_uri(cfg.MLFLOW_HOST)
            mlflow.set_experiment(cfg.MLFLOW_NAME_EXPERIMENT)
            with mlflow.start_run():
                model = CatBoostRegressor(**cfg.MODEL_PARAMS)
                model.fit(X_train, y_train, eval_set=(X_val, y_val), cat_features=cat_features)
                logger.info("MODEL HAS BEEN RETRAINED")

                metrics = self._get_model_score(y_test, model.predict(X_test))

                mlflow.log_params(cfg.MODEL_PARAMS)
                mlflow.log_metric("MAE", metrics[0])
                mlflow.log_metric("MAPE", metrics[1])
                mlflow.catboost.log_model(cb_model=model,
                                          artifact_path='mlflow',
                                          registered_model_name='cb_default'
                                          )
                mlflow.end_run()

        except exc.DBConnectionFailed:
            raise
        except exc.RatingEquationFailed:
            raise
        except exc.TrainTestSplitFailed:
            raise
        except exc.NotItemsWithoutRating:
            raise
        except exc.EstimateModelFailed:
            raise
        else:
            self._save_model(model, cfg.PATH_TO_SAVE_MODEL)
            logger.info("MODEL HAS BEEN SAVE")
            return metrics


if __name__ == "__main__":
    db = Database()
    model_retrain = ModelRetraining(database=db, save_path=cfg.PATH_TO_SAVE_MODEL)
    model_retrain.start_model_retraining()



