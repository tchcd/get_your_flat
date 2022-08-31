import logging
from src.logcfg import logger_cfg

logging.config.dictConfig(logger_cfg)
logger = logging.getLogger('logger')


# Parser Exceptions
class ParserError(Exception):
    def __init__(self, msg=''):
        self.msg = msg
        logger.exception(msg)

    def __str__(self):
        return self.msg


class ParsingNotComplete(ParserError):
    def __init__(self):
        super().__init__(
            msg="PARSER HAS BEEN FAILED!"
        )


class TransformDataNotComplete(ParserError):
    def __init__(self):
        super().__init__(
            msg="DATA TRANSFORMATION HAS BEEN FAILED"
        )


# Database Exceptions
class DatabaseError(Exception):
    def __init__(self, msg=''):
        self.msg = msg
        logger.exception(msg)

    def __str__(self):
        return self.msg


class AddToDBFailed(DatabaseError):
    def __init__(self):
        super().__init__(
            msg="ADD ITEMS TO DATABASE HAS BEEN FAILED"
        )


class DBConnectionFailed(DatabaseError):
    def __init__(self):
        super().__init__(
            msg="DATABASE CONNECTION FAILED"
        )


class UpdateDBItemsFailed(DatabaseError):
    def __init__(self):
        super().__init__(
            msg="UPDATE ITEM VALUES HAS BEEN FAILED"
        )


# Model Retraining Exceptions
class RetrainingModelError(Exception):
    def __init__(self, msg=''):
        self.msg = msg
        logger.exception(msg)

    def __str__(self):
        return self.msg


class TrainTestSplitFailed(RetrainingModelError):
    def __init__(self):
        super().__init__(
            msg="TRAIN TEST SPLIT ERROR"
        )


class NotItemsWithoutRating(RetrainingModelError):
    def __init__(self):
        super().__init__(
            msg="NO ITEMS IN DATAFRAME FOR RETRAINING MODEL"
        )


class EstimateModelFailed(RetrainingModelError):
    def __init__(self):
        super().__init__(
            msg="THE MODEL CANNOT BE EVALUATED"
        )


class RatingEquationFailed(RetrainingModelError):
    def __init__(self):
        super().__init__(
            msg="RATING EQUATION CANNOT BE APPLIED"
        )
