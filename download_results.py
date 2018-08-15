"""
Download all event results from competitions.json.

"""

import os
import json

COMPS_FILE = 'competitions.json'
RESULTS_DOWNLOAD_DIR = 'raw_results'

def sanitize_dir_name(s):
    """Convert the given string to an appropriate directory name.
    Make everything lower case, replace spaces with underscores,
    remove quotes/apostrophes."""
    invalid_chars=["'", '"']
    
    s = s.lower()
    s = s.replace(' ', '_')
    
    for invalid_char in invalid_chars:
        s = s.replace(invalid_char, '')

    return s

if not os.path.exists(COMPS_FILE):
    raise Exception("'{}' does not exist".format(COMPS_FILE))

with open(COMPS_FILE) as f:
    content = f.read()
comps = json.loads(content)

for comp in comps:
    dir_name = sanitize_dir_name(comp['name'] + '-' + comp['date'])
    print("{}  --->  {}".format(comp['name'], dir_name))
    #for event in comp['events']:
        #print("    Weapon: {}. Url: {}".format(event['weapon'], event['url']))
