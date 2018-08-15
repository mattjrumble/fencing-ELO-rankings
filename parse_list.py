"""
Parse the results list,
"""

import json
            
results_file = 'competitions.json'

with open(results_file) as f:
    content = f.read()
comps = json.loads(content)

for comp in comps:
    print("Name: {} ({})".format(comp['name'], comp['date']))
    for event in comp['events']:
        print("    Weapon: {}. Url: {}".format(event['weapon'], event['url']))
