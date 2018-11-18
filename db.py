#!/user/bin/env python3.6

import os
import urllib.request
import json
from pymongo import MongoClient

from helpers.log_to_logfile import add_to_log

OTS_API_KEY = os.environ['OTS_API_KEY']
DB_URI = os.environ['DB_URI']

client = MongoClient(DB_URI)
db = client.ots_database
collection = db.ots_collection

def load_api_data (API_URL):
    """
    Download data from API_URL
    return: json
    """

    #actual download
    with urllib.request.urlopen(API_URL) as url:
        api_data = json.loads(url.read().decode())

    #testing data
    ##with open('nrw.json', 'r') as testing_set:
    ##    api_data = json.load(testing_set)

    return api_data

def store_in_db(story):
    """
    Check if story['id'] is already in database. If not: store story in db
    Return: True if new story added, False if story already in db
    """    
    if db.stories.find_one({'id': story['id']}):
        return False
    else:
        db.stories.insert_one(story)
        return True

def get_from_db(id):
    """
    Retrieve story from db based on id
    Return: story as dict (return warning message if no story is found)
    """
    if db.stories.find_one({'id': id}):
        return db.stories.find_one({'id': id})
    else:
        message = f'No story with id {id} found!'
        return message


def update (region, limit):
    """
    Generate API-URL, download stories and store new stories in db
    return: A list of ids of new items (list is empty if nothing new discovered)
    ToDo: Accept more than one region (currently only first region in list of regions)
    """
    region = region[0].lower()  #region always has to be lowercase. Currently only considering first region provided
    API_URL = f'https://api.presseportal.de/api/article/publicservice/region/{region}?api_key={OTS_API_KEY}&format=json&limit={limit}'

    try:  #  In case api returns an empty doc and JSONDecodeError occurs: skip this polling cycle
        api_data = load_api_data(API_URL)
        
        new_stories = set()
        
        for story in api_data['content']['story']:
            story_title = story['title'].replace('\n', ' ').replace('\r', '')
            if store_in_db(story):
                #print (f'Added to db: "{story_title}"')
                new_stories.add(story['id'])
            #else:
                #print(f'Already in db: "{story_title}"')
    
    except json.decoder.JSONDecodeError as e:
        print(e)
        add_to_log(e, 'error')

    return new_stories 
