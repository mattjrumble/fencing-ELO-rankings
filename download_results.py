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

def main():

    if not os.path.exists(COMPS_FILE):
        raise Exception("'{}' does not exist".format(COMPS_FILE))

    with open(COMPS_FILE) as comps_file:
        content = comps_file.read()
    comps = json.loads(content)

    for comp in comps:
        short_date = long_dtime_to_short(comp['date'])
        comp_dir = sanitize_dir_name(short_date + '_' + comp['name'])

        comp_dir_path = os.path.join(COMPS_DOWNLOAD_DIR, comp_dir)

        os.makedirs(comp_dir_path, exist_ok=True)

if __name__ == '__main__':
    main()
