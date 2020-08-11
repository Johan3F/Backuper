import os
import sys
import stat
import json
import shutil
import logging
import argparse
import datetime

from re import search, compile

from dirsync import sync
from pathlib import Path

CONFIGURATION_FILE_PATH = r'conf.json'
DATETIME_FORMAT = r'%Y%m%dT%H%M%S'
ROOT_SUBFOLDER = 'backup_{}'.format(
    datetime.datetime.now().replace(microsecond=0).strftime(DATETIME_FORMAT))


def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    '''
    Handler for unhandled exceptions that will write to the logs.
    @StolenFrom: https://www.scrygroup.com/tutorial/2018-02-06/python-excepthook-logging/
    '''
    if issubclass(exc_type, KeyboardInterrupt):
        # call the default excepthook saved at __excepthook__
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Unhandled exception: ", exc_info=(
        exc_type, exc_value, exc_traceback))


sys.excepthook = handle_unhandled_exception


def retrieve_configuration_from_file(file_path: Path):
    '''
    Gets information from the given file, and return an array of strings 
    '''
    try:
        json_file = {}
        with open(file_path) as raw_file:
            json_file = json.load(raw_file)

        # Verify that we have the mandatory field in the configuration file
        for field in ['output_folder', 'folders_to_backup', 'history_level']:
            if field not in json_file:
                raise RuntimeError('{}'.format(field))
        output_folder = Path(json_file['output_folder'])
        history_level = json_file['history_level']

        # Build the folders mapping information
        base_target = output_folder / ROOT_SUBFOLDER
        folders_to_backup = []
        for element in json_file['folders_to_backup']:
            target = base_target / \
                element['subfolder'] if 'subfolder' in element else base_target

            for path in element['folders']:
                source = Path(path)
                folders_to_backup.append(
                    {"source": source, "target": Path(target)})
    except RuntimeError as e:
        logging.critical(
            'Missing field {} from the configuration file'.format(e))
        raise e
    except json.JSONDecodeError as e:
        logging.critical(
            'Error when reading the configuration file: {}'.format(e))
        raise e

    return output_folder, history_level, folders_to_backup


def remove_old_backup(output_folder: Path, history_level: int):
    '''
    Removes the oldest backups stored in the output folder if there are more that history_level
    '''
    # Error handler for files that are marked as read-only
    def on_delete_error(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)

    # Lists all backups and sort then by creation date
    folder_in_output_folder = sorted(
        Path(output_folder).iterdir(), key=os.path.getmtime, reverse=True)
    folder_in_output_folder = [f for f in folder_in_output_folder if search(
        r'backup_\d\d\d\d\d\d\d\dT\d\d\d\d\d\d', f.name) is not None]

    while len(folder_in_output_folder) >= history_level:
        # Removing the oldest folder and it's content. Let except so the error is catch by the launcher
        folder_to_remove = folder_in_output_folder.pop()

        logging.info('Removing folder {}'.format(folder_to_remove))
        shutil.rmtree(folder_to_remove, onerror=on_delete_error)


def store_backup(folder_to_backup: list):
    '''
    Stores every folder into the ourput folder, concatenating current date time to keep history
    '''
    def get_duplicate_suffix(path: Path, name: str) -> str:
        '''
        Returns a suffix (N) where N is the number of duplicate, or empty if there's none
        '''
        suffix = ''
        if path.exists():
            regex = compile(name+r'[\(\d+\)]*')
            folders_in_path = [item.stem for item in path.iterdir()]

            duplicates = list(filter(regex.match, folders_in_path))
            if duplicates:
                suffix = '({})'.format(len(duplicates))

        return suffix

    logging.info('Beginning backup')
    for folder in folder_to_backup:
        # If there's a duplicate, add (N) to the target name
        duplicate_sufix = get_duplicate_suffix(
            folder['target'], folder['source'].stem)

        sync(folder['source'], folder['target'] / (folder['source'].stem + duplicate_sufix), 'sync',
             purge=True, create=True, verbose=True)


def process(file_path: Path):
    '''
    Retrives data from file, and syncs folders into a new folder with current datetime
    '''
    # Retrieving configuration from file
    output_folder, history_level, folders_to_backup = retrieve_configuration_from_file(
        file_path)

    # Removing the oldest backup in case there are more than history_level
    remove_old_backup(output_folder, history_level)

    # Actually storing the backup
    store_backup(folders_to_backup)


def main():
    '''
    Deals with input arguments and calles process
    '''
    logging.basicConfig(filename='las_run.log',
                        filemode='w+', level=logging.DEBUG)

    parser = argparse.ArgumentParser(
        description='Synchronizes all folders and files given in a txt file, into the destiny folder')
    parser.add_argument('--file_path', type=Path, default=Path(CONFIGURATION_FILE_PATH),
                        help='Path to the file that contains information. The first line of that file, is the destiny folder')

    args = parser.parse_args()

    process(args.file_path)


if __name__ == '__main__':
    main()
