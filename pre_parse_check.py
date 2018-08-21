"""
Check all the raw results are separately into weapons correctly,
and are in supported formats.
"""

import os

COMPS_DOWNLOAD_DIR = 'comps'
METAFILE = 'metafile.json'
RESULTS_FILE = 'results'

ALL_WEAPONS = ['ME', 'MF', 'MS', 'WE', 'WF', 'WS']
SUPPORTED_FORMATS = ['txt', 'htm', 'html', 'pdf', 'csv']

class NoExtensionFound(Exception):
    """Exception for when an extension cannot be found from
    the given filename."""
    pass

def get_file_extension(filename):
    """Return the file extension from a given filename.
    If no file extension found, raise a NoExtensionFound exception."""
    if '.' not in filename:
        raise NoExtensionFound("Unable to get file extension from: '{}'".format(filename))

    extension = filename.split('.')[-1]
    return extension

def main():
    for comp_dir in os.listdir(COMPS_DOWNLOAD_DIR):
        comp_dir_path = os.path.join(COMPS_DOWNLOAD_DIR, comp_dir)
        for event in os.listdir(comp_dir_path):
            if event not in ALL_WEAPONS:
                print("Event '{}' in '{}' is not a recognised weapon.".format(event, comp_dir_path))
                continue
            event_path = os.path.join(comp_dir_path, event)
            results_files = [file for file in os.listdir(event_path) if file.startswith(RESULTS_FILE)]
            if not results_file:
                print("No results file found in '{}'".format(event_path))
                continue
            elif len(results_files) > 1:
                print("Multiple results files found in '{}'".format(event_path))
                continue

            results_file = results_files[0]
            results_path = os.path.join(event_path, results_file)

            try:
                ext = get_file_extension(results_file)
            except NoExtensionFound as exc:
                print(exc)
                continue
            if ext not in SUPPORTED_FORMATS:
                print("Unsupported extension '{}' in '{}'".format(ext, results_path))
                continue



if __name__ == '__main__':
    main()
    