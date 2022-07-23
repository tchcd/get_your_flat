# Сделать кучку ексепшенов для try/except
class MyEx(Exception):
    """Exception"""

    pass


class prepare_data_failed(Exception):
    pass


class db_connect_fail(Exception):
    pass


class file_write_fail(Exception):
    pass
