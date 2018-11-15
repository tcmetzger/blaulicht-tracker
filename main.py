#!/user/bin/env python3.6

import time

from config import STATE_FILTER, DELAY
import db

if __name__ == '__main__':
    while True:
        db.update(STATE_FILTER)
        print(f'Sleeping for {DELAY} seconds.')
        time.sleep(DELAY)
