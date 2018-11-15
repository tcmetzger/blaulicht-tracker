#!/user/bin/env python3.6

# imports go here

from config import STATE_FILTER
import db

if __name__ == '__main__':
    db.update(STATE_FILTER)
