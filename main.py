#!/user/bin/env python3.6

import time
from datetime import datetime

from config import STATE_FILTER, DELAY, DOWNLOAD_LIMIT
import db

if __name__ == '__main__':
    while True:
        new_stories=db.update(STATE_FILTER, DOWNLOAD_LIMIT)
        if len(new_stories) > 0:
            print(f'Found new stories: {new_stories}:')
            for item in new_stories:
                story = db.get_from_db(item)
                datetime_published = datetime.strptime(story['published'], '%Y-%m-%dT%H:%M:%S%z')
                print(f'{datetime_published.strftime("%d.%m.%Y %H:%M:%S")} {story["title"]} ({story["url"]})')
        else:
            print('No new stories found.')
        print(f'Sleeping for {DELAY} seconds.')
        time.sleep(DELAY)
