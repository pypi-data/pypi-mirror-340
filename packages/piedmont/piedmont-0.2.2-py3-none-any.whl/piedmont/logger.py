import logging
import logging.config
import typing as t
import sys
import os
import tempfile

LOG_PATH = os.path.join(tempfile.gettempdir, 'piedmont.log')


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': "[Piedmont][%(levelname)s]:\t%(message)s"
        },
        'detailed': {
            'format': "$ %(asctime)s [%(name)s][%(levelname)s][%(threadName)s:%(process)d]::%(module)s::\t%(message)s"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': sys.stdout
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': LOG_PATH,
            'formatter': 'detailed',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        }
    },
    'loggers': {
        'piedmont': {
            'level': 'ERROR',
            'handlers': ['file', 'console'],
            'propagate': False
        },
    }
}


logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger('piedmont')
console = logging.getLogger('piedmont-console')


def set_dev_mode(flag=True):
    if flag:
        logger.setLevel(logging.DEBUG)
        logger.debug(
            f'\n{"=" * 48}\n{">"*15} PIEDMONT DEV LOG {"<"*15}\n{"=" * 48}'
        )
    else:
        logger.setLevel(logging.CRITICAL)
