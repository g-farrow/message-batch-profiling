import logging
from os import environ
from aws_xray_sdk import global_sdk_config


logger = logging.getLogger('message-batch-profiling')
logger.setLevel(environ.get('LOG_LEVEL', 'DEBUG'))

global_sdk_config.set_sdk_enabled(True)
