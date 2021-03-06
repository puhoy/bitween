import os
import yaml

import logging.config

def setup_logging(
        default_path='logging.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """
    Set up logging
    Called once at program start

    read the config from logging.yml but set console loglevel to default_level
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f)
            config['handlers']['console']['level'] = default_level
        logging.config.dictConfig(config)

    logging.basicConfig(level=default_level)