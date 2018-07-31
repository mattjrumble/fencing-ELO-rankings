import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# Most of the results are in these predictable HTML forms, so we can get most of the results quite easily!

import requests
import pandas as pd
import enum

urls = [
            "http://britishfencing.com/uploads/files/lp_summer_open_2017_me.htm",
            "http://britishfencing.com/uploads/files/e6_newcastle_mens_epee_2017.html",
            "http://britishfencing.com/uploads/files/hampshire_openmens_foil_17.htm"
       ]
url = urls[2]
html = requests.get(url).text
df = pd.read_html(html)[1]

class ColumnType(enum.Enum):
    UNKNOWN = 0
    RANK = 1
    FIRST_NAME = 2
    SURNAME = 3
    MEMBERSHIP_NO = 4
    CLUB = 5
    COUNTRY = 6

def deduce_column_type(header):
    # TODO: If name column but no surname column, all the name must be in that value, so try to split that by either spaces or commas.
    # Do multiple passes. 'member' might be in 'membership number', or maybe 'members club' at more of a stretch. Rule out the obvious ones first.
    # If the table doesn't have anything that looks like a rank column and a name column, give up on that table and search for others I suppose.

    header = header.lower()
    if any(x in header for x in ['rank', 'place', 'result']):
        return ColumnType.RANK
    if any(x in header for x in ['first name', 'forename']):
        return ColumnType.FIRST_NAME
    if any(x in header for x in ['name', 'surname', 'last name']):
        return ColumnType.SURNAME
    if any(x in header for x in ['bfa', 'license', 'licence', 'member']):
        return ColumnType.MEMBERSHIP_NO
    if any(x in header for x in ['club']):
        return ColumnType.CLUB
    if any(x in header for x in ['country']):
        return ColumnType.COUNTRY
    return ColumnType.UNKNOWN
    
    
# Deduce what the columns are
# print(df)
for heading in df.iloc[0]:
    print("{} - {}".format(heading, deduce_column_type(heading).name))
