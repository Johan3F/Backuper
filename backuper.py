import os
import json
import shutil
import argparse
import datetime

from re import search
from dirsync import sync
from pathlib import Path

CONFIGURATION_FILE_PATH = 'conf.json'
DATETIME_FORMAT = '%Y%m%dT%H%M%S'


def retrieve_from_file(file_path: Path):
    '''
    Gets information from the given file, and return an array of strings 
    '''
    json_file = {}
    with open(file_path) as raw_file:
        json_file = json.load(raw_file)

    # Verify that we have everything we need in the configuration file
    for field in ['output_folder', 'folders_to_backup']:
        if field not in json_file:
            raise RuntimeError(
                '{} is missing from the configuration file'.format(field))
    output_folder = Path(json_file['output_folder'])
    folders_to_backup = [Path(folder)
                         for folder in json_file['folders_to_backup']]

    return output_folder, folders_to_backup


def remove_old_backup(output_folder, history_level):
    '''
    Removes the oldes backup stored in the output folder if there are more that history_level
    '''
    # Lists all backups and sort then by creation date
    folder_in_output_folder = sorted(
        Path(output_folder).iterdir(), key=os.path.getmtime, reverse=True)
    folder_in_output_folder = [f for f in folder_in_output_folder if search(
        'backup_\d\d\d\d\d\d\d\dT\d\d\d\d\d\d', f.name) is not None]

    while len(folder_in_output_folder) >= history_level:
        # Removing the oldest folder and it's content. Let except so the error is catch by the launcher
        folder_to_remove = folder_in_output_folder.pop()

        shutil.rmtree(folder_to_remove)


def store_backup(output_folder, folder_to_backup, now):
    '''
    Stores every folder into the ourput folder, concatenating current date time to keep history
    '''
    for folder in folder_to_backup:
        sync(folder, output_folder / 'backup_{}'.format(now.strftime(DATETIME_FORMAT)) / folder.stem, 'sync',
             purge=True, create=True, verbose=True)


def process(file_path: Path, history_level: int):
    '''
    Retrives data from file, and syncs folders into a new folder with current datetime
    '''
    # Retrieving configuration from file
    output_folder, folder_to_backup = retrieve_from_file(file_path)

    # Getting current datetime to create a folder with this name to store this backup
    now = datetime.datetime.now().replace(microsecond=0)

    # Removing the oldest backup in case there are more than history_level
    remove_old_backup(output_folder, history_level)

    # Actually storing the backup
    store_backup(output_folder, folder_to_backup, now)


def main():
    '''
    Deals with input arguments and calles process
    '''
    parser = argparse.ArgumentParser(
        description='Synchronizes all folders and files given in a txt file, into the destiny folder')
    parser.add_argument('--file_path', type=Path, default=Path(CONFIGURATION_FILE_PATH),
                        help='Path to the file that contains information. The first line of that file, is the destiny folder')
    parser.add_argument('--history_level', type=int, default=10,
                        help='Number of backups to safe before starting to delete the oldest one(s)')

    args = parser.parse_args()

    process(args.file_path, args.history_level)


if __name__ == '__main__':
    main()
