# Сделать кучку ексепшенов для try/except
class MyEx(Exception):
    """Exception"""

    pass


class prepare_data_failed(Exception):
    pass

class flat_not_collected(Exception):
    pass

class parse_data_failed(Exception):
    pass

class db_data_transfer_failed(Exception):
    pass

class db_connect_failed(Exception):
    pass


class file_write_fail(Exception):
    pass
