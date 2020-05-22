import argparse

from dirsync import sync
from pathlib import Path

CONFIGURATION_FILE_PATH = 'conf.txt'


def retrieve_from_file(file_path: Path):
    '''
    Gets information from the given file, and return an array of strings 
    '''
    lines = list(file_path.read_text().splitlines())
    lines = [Path(line) for line in lines]

    return lines[0], lines[1:]


def process(file_path: Path):
    '''
    Retrives data from file, and syncs folders
    '''
    output, to_backup = retrieve_from_file(file_path)

    print('Storing into: "%s"' % output)
    for folder in to_backup:
        sync(folder, output / folder.stem, 'sync',
             purge=True, create=True, verbose=True)


def main():
    '''
    Deals with input arguments and calles process
    '''
    parser = argparse.ArgumentParser(
        description='Synchronizes all folders and files given in a txt file, into the destiny folder')
    parser.add_argument('--file_path', type=Path, default=Path(CONFIGURATION_FILE_PATH),
                        help='Path to the file that contains information. The first line of that file, is the destiny folder')

    args = parser.parse_args()

    process(args.file_path)


if __name__ == '__main__':
    main()
