#!/user/bin/env python3.6

import yaml

with open('config.yml', 'r') as fp:
    CONFIG = yaml.safe_load(fp.read())

STATE_FILTER = CONFIG['STATE_FILTER']
DELAY = int(CONFIG['DELAY'])
DOWNLOAD_LIMIT = CONFIG['DOWNLOAD_LIMIT']
