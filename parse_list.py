"""
Parse the results list,
"""

import json
            
results_list = 'results-2017-18.json'

with open(results_list) as f:
    content = f.read()
    
comps = json.loads(content)

for comp in comps:
    print("Name: {}".format(comp['name']))
    print("Date: {}".format(comp['date']))
    for event in comp['events']:
        if 'supported' in event and not event['supported']:
            print("    Event not supported")
            continue
        print("    Weapon: {}. Url: {}".format(event['weapon'], event['url']))
