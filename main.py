#!/user/bin/env python3.6

import time

from config import STATE_FILTER, DELAY
import db

if __name__ == '__main__':
    while True:
        new_stories=db.update(STATE_FILTER)
        if len(new_stories) > 0:
            print(f'Found new stories: {new_stories}:')
            for item in new_stories:
                story = db.get_from_db(item)
                print(story['title'])
        else:
            print('No new stories found.')
        print(f'Sleeping for {DELAY} seconds.')
        time.sleep(DELAY)
