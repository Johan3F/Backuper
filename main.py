import argparse
import datetime
from dirsync import sync
from pathlib import Path

CONFIGURATION_FILE_PATH = 'conf.txt'
DATETIME_FORMAT = '%Y%m%dT%H%M%S'


def retrieve_from_file(file_path: Path):
    '''
    Gets information from the given file, and return an array of strings 
    '''
    lines = list(file_path.read_text().splitlines())
    lines = [Path(line) for line in lines]

    return lines[0], lines[1:]


def store_backup(output_folder, folder_to_backup, now):
    '''
    Stores every folder into the ourput folder, concatenating current date time to keep history
    '''
    print('Storing into: "%s"' % output_folder)
    for folder in folder_to_backup:
        sync(folder, output_folder / now.strftime(DATETIME_FORMAT) / folder.stem, 'sync',
             purge=True, create=True, verbose=True)


def process(file_path: Path, history_level: int):
    '''
    Retrives data from file, and syncs folders into a new folder with current datetime
    '''
    # Retrieving configuration from file
    output_folder, folder_to_backup = retrieve_from_file(file_path)

    # Getting current datetime to create a folder with this name to store this backup
    now = datetime.datetime.now().replace(microsecond=0)

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
                        help='Number of backups to safe before starting to delete the oldest one')

    args = parser.parse_args()

    process(args.file_path, args.history_level)


if __name__ == '__main__':
    main()
