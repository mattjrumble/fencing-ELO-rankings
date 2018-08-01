import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# Most of the results are in these predictable HTML forms, so we can work just using them to start with. 

import requests
import pandas as pd
from enum import Enum

class ColumnType(Enum):
    UNKNOWN = 0
    RANK = 1
    FIRST_NAME = 2
    SURNAME = 3
    LICENSE = 4
    CLUB = 5
    COUNTRY = 6
    
def reduced_df_from_df_list(df_list):
    # Given a list of dataframes, try each one in turn to see if it looks like the final results. If we find one, return
    # the reduced form of that dataframe. If we don't find such a dataframe, return None.
    for df in df_list:
        reduced = reduce_df(df)
        if reduced is not None:
            return reduced
        return 0 # Testing
    return None
    
def reduce_df(df):
    # Given a dataframe, check that it contains all the required column types. If so, remove any columns we don't care
    # about, and return the reduced dataframe. If not, return None.
    
    # TODO: Make a dict of enums or something for a nicer way to do these bools.
    found_rank = False
    found_first_name = False
    found_surname = False
    
    found_license = False
    found_club = False
    found_country = False
    
    for heading in df.iloc[0]:
        
    # We need to return columns of rank, first name, surname. If available, also return license, club, country.
    # Are there any unambiguous columns, like exactly 'First name' or 'Club'/'Club(s)'. If so, add them to a
    # new dataframe and stop searching for them.
    # Now, given those out of the way, is anything that was previously ambiguous now not? Like 'name', now that
    # 'first name' is already found. 
    # If we still don't have first name and surname, but we have a name column, derive them from that, assuming
    # either commas or spaces.
    # If we don't have rank, first name and surname here, give up on this dataframe.
    # Make best guess for everything else. Use 'does club appear anywhere in the header' rather than 'is header
    # exactly club'. 'member' might be in 'membership number', or maybe 'members club' at more of a stretch, so
    # check for 'club' before checking for 'member' or 'number'.

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
    
urls = [
        #"http://britishfencing.com/uploads/files/lp_summer_open_2017_me.htm",
        "http://britishfencing.com/uploads/files/e6_newcastle_mens_epee_2017.html",
        #"http://britishfencing.com/uploads/files/hampshire_openmens_foil_17.htm",
       ]

for url in urls:
    html = requests.get(url).text
    df_list = pd.read_html(html)
    df = reduced_df_from_df_list(df_list)
