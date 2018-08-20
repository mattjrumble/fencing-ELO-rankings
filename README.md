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

2.  TODO: Download the results from every event in competitions.json. Have a metafile for each event.