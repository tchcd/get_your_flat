# Parser Exceptions
class ParserError(Exception):
    pass


class ParsingNotComplete(ParserError):
    super().__init__(
        "PARSER HAS BEEN FAILED!"
    )


class TransformDataNotComplete(ParserError):
    super().__init__(
        "DATA TRANSFORMATION HAS BEEN FAILED"
    )


# Database Exceptions
class DatabaseError(Exception):
    pass


class AddToDBFailed(DatabaseError):
    super().__init__(
        "ADD ITEMS TO DATABASE HAS BEEN FAILED"
    )


class DBConnectionFailed(DatabaseError):
    super().__init__(
        "DATABASE CONNECTION FAILED"
    )


class UpdateDBItemsFailed(DatabaseError):
    super().__init__(
        "UPDATE ITEM VALUES HAS BEEN FAILED"
    )


# Model Retraining Exceptions
class RetrainingModelError(Exception):
    pass


class TrainTestSplitFailed(RetrainingModelError):
    super().__init__(
        "TRAIN TEST SPLIT ERROR"
    )


class NotItemsWithoutRating(RetrainingModelError):
    super().__init__(
        "NO ITEMS IN DATAFRAME FOR RETRAINING MODEL"
    )


class EstimateModelFailed(RetrainingModelError):
    super().__init__(
        "THE MODEL CANNOT BE EVALUATED"
    )


class RatingEquationFailed(RetrainingModelError):
    super().__init__(
        "RATING EQUATION CANNOT BE APPLIED"
    )
