import logging

logging.basicConfig(level=logging.DEBUG)

from configs import load_configs, options, NcmsConfig

assert  options.debug is False

load_configs('../ncms_data/config.dev.json')

assert options.debug is True

