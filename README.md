# Fencing ELO rankings

The aim is to apply an ELO ranking system to British Fencing senior individual results to get a more accurate indicator of true strength than the official rankings (which are designed more to encourage participation than to truly reflect the strength of the fencers).

# Process

1.  Get all the senior individual competition info from the following pages:

        https://www.britishfencing.com/results-rankings/2016-2017-event-results-archive/
        https://www.britishfencing.com/results-rankings/2017-18-event-results-archives/
    
    Manually convert the info on the pages into a consistent format in competitions.json.
    
    Every competition should have a name, date and list of events.
    Every event should have a weapon and download url.
    Event can optionally have a format to explicitly describe the file format at the download url, and any extra_info of interest about the event itself.

2.  For each event in competitions.json, download the raw results and write an associated metafile with all information about the event ('download_results.py').

3.  Run a check over all the downloaded results to see if they're all in supported formats and have been separated into individual weapons correctly ('pre_parse_check.py'). If any of them fail the checks, convert them into supported formats/separate into individual weapons manually, otherwise they will be ignored in the ranking calculations.

4.  TODO: Parse all results into a consistent format.

5.  TODO: Maths
