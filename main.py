#!/user/bin/env python3.6

import time
from datetime import datetime

from config import STATE_FILTER, DELAY, DOWNLOAD_LIMIT
from helpers.log_to_logfile import add_to_log
from helpers.send_to_slack import message_to_slack, create_attachment
import db
import regex_filters

if __name__ == '__main__':
    while True:
        new_stories=db.update(STATE_FILTER, DOWNLOAD_LIMIT)
        if len(new_stories) > 0:
            print(f'Found new stories: {new_stories}:')
            for item in new_stories:
                story = db.get_from_db(item)
                datetime_published = datetime.strptime(story['published'], '%Y-%m-%dT%H:%M:%S%z')
                story_title = story['title'].replace('\n', ' ').replace('\r', '')
                print(f'{datetime_published.strftime("%d.%m.%Y %H:%M:%S")} {story_title} ({story["url"]})')
                filter_result = regex_filters.check_filter(item)
                if filter_result:
                    print(f'+++ {" ".join(str(s) for s in filter_result)} +++')
                    output_message = f'{datetime_published.strftime("%d.%m.%Y %H:%M:%S")} {story_title} ({story["url"]}) [{" ".join(str(s) for s in filter_result)}]'
                    if 'Image' in str(filter_result): # Create attachment for slack for items with image 
                        attached = create_attachment(story)
                        message_to_slack(output_message, attached)
                    else: # Send straight to slack if no image present
                        message_to_slack(output_message)
                    # message_to_slack(f'{datetime_published.strftime("%d.%m.%Y %H:%M:%S")} {story_title} ({story["url"]}) [{" ".join(str(s) for s in filter_result)}]')
                    add_to_log(f'{" ".join(str(s) for s in filter_result)}, {story["url"]}', 'info')
        else:
            print('No new stories found.')
        print(f'Sleeping for {DELAY} seconds.')
        time.sleep(DELAY)
