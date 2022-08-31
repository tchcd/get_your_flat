import logging.config
import cfg

logger_cfg = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base_formatter': {
            'format': '{asctime} - {levelname} - {name} - {module} - {message}',
            'style': '{'
        },
        'error_formatter': {
            'format': '{asctime} - {levelname} - {name} - {module}  - {funcName} - {lineno} - {message}',
            'style': '{'
        },
    },
    'handlers': {
        'console_info': {
            'level': 'INFO',
            'formatter': 'base_formatter',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        },
        'file_info': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'base_formatter',
            'filename': cfg.INFO_LOG_FILE,
            'mode': 'a'
        },
        'console_error': {
            'level': 'ERROR',
            'formatter': 'error_formatter',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        },
        'file_error': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'formatter': 'error_formatter',
            'filename': cfg.ERRORS_LOG_FILE,
            'mode': 'a'
        },

    },
    'loggers': {
        'logger': {
            'level': 'INFO',
            'handlers': ['console_info', 'file_info', 'console_error', 'file_error']
        },
    }
    # 'filters': {}
}

if __name__ == "__main__":
    pass
