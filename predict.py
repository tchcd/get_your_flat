# здесь мы достаем из БД новые объявления
# делаем для них предикт
# добавляем предикты в БД (или перезаливаем в БД объекты)

from database import Database
from catboost_daily_model import get_daily_predict

# 1. get_cards_from_db - не размеченые объекты из БД.
# 2. start_catboost - применяет алгоритм к полученным объектам
# 3. отдает размеченные объекты в функцию миграции из модуля migration?


#Не знаю, видимо обернуть это все в функцию predict() и запускать из main

# Получаем из БД не размеченные новые карточки, после парсера
not_evaluated_cards = Database.get_not_evaluated_cards()

# Применяем CatBoost к неразмеченным
predicted_cards = catboost_daily(not_evaluated_cards)

# Заливаем в БД
Database.add_daily_avito_cards_to_db(predicted_cards)
