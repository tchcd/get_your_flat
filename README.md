# Get Your Flat

Бот на фласке, который отправляет в телеграм подходящие для покупки квартиры.
1. Парсит с авито подходящие квартиры(Selenium выставляет фильтры, собирает линки, заходит в карточки и собирает данные)
2. Данные объявлений падают в SQLite БД.
3. Новые объявления, которые еще не были размечены приходят на разметку Кетбусту. Он проставляет им скор и в БД обнавляется колонка со скором.
4. По запросу из ТГ фласк отправляет ТОП1 по скору в бота.
5. Отправленным в бот объявлениям в БД обновляется колонка shown = 1. Отправляются только те, у которых shown = 0.

Структура проекта:

src/data/ - Все, что связано с парсингом и подготовкой данных:
	<br>&nbsp;&nbsp;&nbsp;&nbsp; avito_etl.py - ETL скрипт, который запускает скрипты парсера и подготовки данных.
	<br>&nbsp;&nbsp;&nbsp;&nbsp; avito_parser_class - Класс парсера. Здесь запускается селенуим, проходит аутентификация на авито, фильтры и вся логика парсинга объявлений.
	<br>&nbsp;&nbsp;&nbsp;&nbsp; avito_daily_script - Склейка для запуска скрипта. Здесь только вызовы функций.
	<br>&nbsp;&nbsp;&nbsp;&nbsp; prepare_data - Валидация и подготовка данных, которые пришли от парсера.

src/models/ - Предикты для новых данных и переобучение модели.
	<br>&nbsp;&nbsp;&nbsp;&nbsp; evaluate_new_items - получает последнюю версию модели, получает не размеченные объявления из БД, делает предикт, обновляет скор объявления в БД.
	<br>&nbsp;&nbsp;&nbsp;&nbsp; weekly_retraining - раз в неделю берет все данные из БД и перетренировывает модель (скоры для таргета y_true размечаются согласно формуле)

src/database.py - Класс Database, создание и подключение к БД, sql запросы.







'Get Your Flat' is a Telegram bot that sends suitable flats for purchase.
- The new data comes after avito parsing and gets into the database.
- The bot has a two models:
	1. CatBoost gradient boosting - evaluates the new flats from database.
	2. Linear Regression - estimate the price of flats based on similar flats. <i>(not ready yet)</i>
- Launch parsing scripts, evaluation of new items and retraining of the CatBoost model occur using AirFlow/MLFlow. <i>(not ready yet)</i>
- The Bot is located on a remote debian server with a docker container.
