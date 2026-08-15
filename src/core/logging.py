import json
import logging
from datetime import datetime
from logging.config import dictConfig

from logtail import LogtailHandler

from src.core.config import settings


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": datetime.fromtimestamp(record.created).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        if record.args and isinstance(record.args, dict):
            log_record.update(record.args)

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record, ensure_ascii=False)


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"json": {"()": JsonFormatter}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "level": "INFO",
        },
        "logtail": {
            "class": LogtailHandler,
            "level": "DEBUG" if settings.IS_DEBUG else "INFO",
            "source_token": settings.logging.LOGTAIL_TOKEN,
            "host": settings.logging.LOGTAIL_HOST,
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console", "logtail"],
            "level": "DEBUG" if settings.IS_DEBUG else "INFO",
            "propagate": False,
        }
    },
}

dictConfig(dict_config)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
