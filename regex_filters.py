#!/user/bin/env python3.6
# TBD: make filters configurable, not hard coded
# These filters are just examples and need to be adapted as need

import re 

import db

def includes_severe_accident(document):
    unfall1 = re.compile(r'((T|t)ödlich).*((U|u)nfall)|((U|u)nfall).*((T|t)ödlich)')
    unfall2 = re.compile(r'((A|a)utobahn)')
    text = document['title'] + ' \n' + document['body']
    if (re.search(unfall1,text)) and (re.search(unfall2,text)):
        return True
    else:
        return False

def includes_media(document):
    """
    Check if media is present (https://api.presseportal.de/doc/value/media) and exclude common stockpics from getting detected as image
    Return set of media types (return empty set if no media is present)
    """
    mediatype = set()
    if 'media' in document.keys():
        exclude_titles = re.compile(r'(Geschwindigkeits(|-)(k|K)ontrollen))')
        if 'image' in document['media'].keys():
            stockpic_caption = re.compile(r'(Symbolbild)|(Symbolfoto)|(Archivbild)|(Archivfoto)')
            if not (re.search(stockpic_caption, str(document['media']['image']))):
                if not (re.search(exclude_titles, document['title'])):
                    mediatype.add('Image')
        if 'document' in document['media'].keys():
            if not (re.search(exclude_titles, document['title'])):
                mediatype.add('Document')
        if 'audio' in document['media'].keys():
            mediatype.add('Audio')
        if 'video' in document['media'].keys():
            mediatype.add('Video')
    return mediatype

def includes_keyword(document):
    """
    Check document for keywords
    Return True if keywords detected
    """
    keywords = re.compile(r'((G|g)emeinsame(|\w) Pressemitteilung)|(Autorennen)|(Lebensretter)')
    fulltext = document['title'] + ' \n' + document['body']
    return (re.search(keywords, fulltext))

def includes_planecrash(document):
    crash = re.compile(r'(Absturz)|(abgestürzt)(\w*)')
    airplane = re.compile(r'(\w*)([Ff]lugzeug)|(Doppeldecker)|(Hubschrauber)|(\w*)([Ll]eichtflieger)')    
    fulltext = document['title'] + ' \n' + document['body']
    if (re.search(crash, fulltext)):
        if (re.search(airplane, fulltext)):
            return True
    else:
        return False 
      
def includes_brawl(document):
    fulltext = document['title'] + ' \n' + document['body']
    if (re.search(re.compile(r'Schlägerei'),fulltext)) and (re.search(re.compile(r'(Gruppe(.|))'),fulltext)) and (re.search(re.compile(r'((V|v)erletzt)'),fulltext)):
            return True

def includes_animal(document):
    animals = re.compile(r'(Ent(e|en)\b)|((Elefant|Zebra|Löwe|Löwin|Raubkatze|Nashorn|Vogelstrauß).*(Zirkus|Zoo|Tierpark))|(Tierrettung)')
    fulltext = document['title'] + ' \n' + document['body']
    return re.search(animals, fulltext)

def check_filter(ots_id):
    """
    Check document in ots_id against a list of regex rules.
    Return set of filters triggered by document in ots_id (returns empty set if no filters were triggered)
    """
    filters = set()
    document = db.get_from_db(ots_id)

    if includes_severe_accident(document):
        filters.add('Severe Accident')

    media = includes_media(document)
    if media:
        filters.add(f'Media ({(media)})')

    key_test = includes_keyword(document)
    if key_test:
        found_keyword = key_test.group(0)
        filters.add(f'Keyword: {found_keyword}')

    if includes_planecrash(document):
        filters.add('Planecrash')

    if includes_brawl(document):
        filters.add('Brawl')

    if includes_animal(document):
        filters.add('Animal')

    return filters

