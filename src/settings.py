class LoggerConfig:
    dictConfig = {
        "version": 1,
        "disable_existing_loggers": True,
        "root": {
            'level': 'INFO',
            'handlers': ['console']
        },
        "formatters": {
            "standard": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            },
            "short": {
                "format": "%(message)s",
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
            "console_info": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "short",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "formatter": "standard",
                "filename": "logs/debug.log",
            },
            "file_info": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "backupCount": 10,
                "formatter": "standard",
                "filename": "logs/info.log",
            },
            "file_error": {
                "level": "ERROR",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "standard",
                "filename": "logs/error.log",
                "maxBytes": 10000,
                "backupCount": 10,
                "delay": "True"
            }
        },
        "loggers": {
            "simple_console": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
            "to_info_file": {
                "handlers": ["console", "file_info"],
                "level": "INFO",
                "propagate": False,
            },
            "to_error_file": {
                "handlers": ["console", "file_error"],
                "level": "ERROR",
                "propagate": False,
            }
        }
    }
