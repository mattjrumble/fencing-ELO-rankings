# Get all the BFA results for the given age/sex/weapon, and put them into CSV files (in their own folder)
# with whatever data the results data has, headed by the competition dates.

import requests
import re
import os
import shutil
from pprint import pprint

def strip_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def strip_suffix(text, suffix):
    if text.endswith(suffix):
        return text[:-len(suffix)]
    return text
    
def extract_section(text, starting_line, ending_line):
    # Returns an array of lines from text, starting and ending at the given lines
    # Ignores leading and trailing whitespace on lines
    result = []
    extracting = False
    for full_line in text.splitlines():
        line = full_line.strip()
        if line == starting_line:
            extracting = True
        if extracting:
            result.append(line)
            if line == ending_line:
                break
    return result
    
def strip_html_tags(text):
    # Given "<blah>foo<bluh>", return "foo"
    return re.sub('<.*?>', '', text)
    
class Comp:
    def __init__(self, name, dates, id):
        self.name = name
        self.dates = dates
        self.id = id
    def __str__(self):
        return "Name = {}. Dates = {}. ID = {}".format(self.name, self.dates, self.id)

results_age = "Senior"
results_sex = "Men's"
results_weapon = "Sabre"

# Get list of competitions
url = 'https://www.britishfencing.com/wp-admin/admin-ajax.php?action=bf_results_load1'
data = { "results_age": results_age, "results_sex": results_sex, "results_weapon": results_weapon, "start": "", "end": "" } 
r = requests.post(url, data=data).text

# Extract the HTML table with the competitions info
table = extract_section(r, '<tbody>', '</tbody>')

# Put the data from the table into objects
comps = []
i = 0
while i < len(table):
    if table[i].startswith('<td>'):
        # Name
        name = table[i]
        name = strip_prefix(name, '<td>')
        name = strip_suffix(name, '</td>')
        # Dates
        dates = table[i+1]
        dates = strip_prefix(dates, '<td>')
        dates = strip_suffix(dates, '</td>')
        # ID
        id = table[i+2]
        id = strip_prefix(id, '<td>')
        id = strip_suffix(id, '</td>')
        id = id.split('\"')[-2]
        
        comps.append(Comp(name, dates, id))
        i += 5
    else:
        i += 1

# Get the results for each comp and put into CSV files, headed by the comp dates
dir = results_age + " " + results_sex + " " + results_weapon
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir)
for comp in comps:
    print("Getting results for {}...".format(comp.name))
    id = comp.id
    url = 'https://www.britishfencing.com/wp-admin/admin-ajax.php?action=bf_results_load2'
    data = { "results_age": results_age, "results_sex": results_sex, "results_weapon": results_weapon, "id": id }
    r = requests.post(url, data=data).text
    table = extract_section(r, '<tbody>', '</tbody>')
    
    out = comp.dates + "\n"
    pattern = re.compile("<t.*>.*</t.*>")
    for line in table:
        if pattern.match(line):
            out += strip_html_tags(line).strip().replace("\\", "") + ","
        elif line == "</tr>":
            out = out[:-1] + "\n"
    if out != "":
        out = out[:-1]
    
    with open("{}\{}.txt".format(dir, comp.name), "w") as text_file:
        text_file.write(out)    
