from dirsync import sync
from pathlib import Path

CONFIGURATION_FILE_PATH = Path('conf.txt')


def retrieve_from_file(file_path: Path):
    '''
    Gets information from the given file, and return an array of strings 
    '''
    lines = list(file_path.read_text().splitlines())
    lines = [Path(line) for line in lines]

    return lines[0], lines[1:]


def main():
    '''
    Retrives data from file, and pass it to process
    '''
    output, to_backup = retrieve_from_file(CONFIGURATION_FILE_PATH)

    print('Storing into: "%s"' % output)
    for folder in to_backup:
        sync(folder, output / folder.stem, 'sync', purge=True, create=True)


if __name__ == '__main__':
    main()
