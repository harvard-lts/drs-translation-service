import structlog
import os, socket
from datetime import datetime

# Reload
if os.environ.get('ENV') == 'development':
    reload = True

# Pre-processing
pre_chain = [
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(),
    structlog.processors.TimeStamper(fmt='iso', utc=True),
]

# Create a log folder for this container if it doesn't exist
container_id = socket.gethostname()
if not os.path.exists(f'/home/appuser/logs/'):
    os.makedirs(f'/home/appuser/logs/')

# Get timestamp
timestamp = datetime.today().strftime('%Y-%m-%d')

# Log config
logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": pre_chain,
        }
    },
    "handlers": {
        "error_console": {
            "class": "logging.FileHandler",
            "formatter": "json_formatter",
            "filename": f"/home/appuser/logs/error_console_{container_id}_{timestamp}.log",
            "mode": "a"
        },
        "console": {
            "class": "logging.FileHandler",
            "formatter": "json_formatter",
            "filename": f"/home/appuser/logs/console_{container_id}_{timestamp}.log",
            "mode": "a"
        }
    },
    "loggers": {
        'gunicorn.error': {
            'handlers': ['console'],
            'level': os.environ.get('APP_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'gunicorn.access': {
            'handlers': ['console'],
            'level': os.environ.get('APP_LOG_LEVEL', 'INFO'),
            'propagate': False,
        }
    }
}
