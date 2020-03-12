import logging
from os import environ

logger = logging.getLogger('message-batch-profiling')
logger.setLevel(environ.get('LOG_LEVEL', 'DEBUG'))
