# Get Your Flat

'Get Your Flat' is a Telegram bot that sends suitable flats for purchase.
- The new data comes after avito parsing and gets into the database.
- The bot has a two models:
	1. CatBoost gradient boosting - evaluates the new flats from database.
	2. Second CatBoost model estimate the price of flats based on similar flats. <i>(not ready yet)</i>
- Launch parsing scripts, evaluation of new items and retraining of the CatBoost model occur using AirFlow/MLFlow.
- The Bot is located on a remote server with a docker container.
