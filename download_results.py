"""
Download all event results from competitions.json.
Each competition has its own directory, and each
weapon event has a directory within that, containing
the results file and metadata file for that event.
"""

import os
import json
from datetime import datetime

COMPS_FILE = 'competitions.json'
METAFILE = 'metafile.json'
COMPS_DOWNLOAD_DIR = 'comps'

def sanitize_dir_name(dir_name):
    """Convert the given string to an appropriate directory name.
    Make everything lower case, replace spaces with underscores,
    remove quotes/apostrophes."""
    invalid_chars = ["'", '"']

    dir_name = dir_name.lower()
    dir_name = dir_name.replace(' ', '_')

    for invalid_char in invalid_chars:
        dir_name = dir_name.replace(invalid_char, '')

    return dir_name

def long_dtime_to_short(dt_str):
    """Convert a datetime in the format '25th October 2016' or
    '25th Oct 2016' into '2016-10-25'."""

    if len(dt_str.split()) != 3:
        raise Exception("Expected 3 words in datetime: '{}'".format(dt_str))

    # Remove 'st'/'nd'/'rd' suffix
    start, end = dt_str.split(' ', 1)
    start = start[:-2]
    dtime_str = start + ' ' + end

    try:
        dtime = datetime.strptime(dtime_str, '%d %B %Y')
    except ValueError:
        dtime = datetime.strptime(dtime_str, '%d %b %Y')

    return dtime.strftime('%Y-%m-%d')

def make_comp_dir(comp):
    """Generate a suitable directory name from the given comp info."""
    short_date = long_dtime_to_short(comp['date'])
    return sanitize_dir_name(short_date + '_' + comp['name'])
    
def verify_path_exists(path):
    """Raise an exception if the given path doesn't exist."""
    if not os.path.exists(path):
        raise Exception("'{}' does not exist".format(path))
       
def get_comps():
    """Get a list of all competition info read
    from COMPS_FILE."""
    verify_path_exists(COMPS_FILE)

    with open(COMPS_FILE) as comps_file:
        content = comps_file.read()
    return json.loads(content)

def write_metafile(dir, comp, event):
    """Write a metafile in the given directory. Use information from both
    the event and the competition as a whole."""
    mf_path = os.path.join(dir, METAFILE)
    
    mf_content = {"name": comp['name'],
                  "date": comp['date'],
                  "weapon": event['weapon'],
                  "url": event['url']}

    with open(mf_path, 'w+') as mf:
        json.dump(mf_content, mf, sort_keys=True, indent=4)
        
def main():

    for comp in get_comps():

        comp_dir = make_comp_dir(comp)
        comp_dir_path = os.path.join(COMPS_DOWNLOAD_DIR, comp_dir)
        os.makedirs(comp_dir_path, exist_ok=True)
        
        for event in comp['events']:
            event_dir_path = os.path.join(comp_dir_path, event['weapon'])
            os.makedirs(event_dir_path, exist_ok=True)
            
            write_metafile(event_dir_path, comp, event)
        

if __name__ == '__main__':
    main()
