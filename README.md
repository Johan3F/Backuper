# Backuper
SimpleBackuper

It's a simple backp program that expects a text file where the first line is the output folder, and the next files and folder to by synced in the output folder.
It will store all folders form the list in a subfolder of the output folder with the current datetime.
It will keep by default only 10 backups,

Example:
conf.txt content:
```
D:\Temp
D:\Music\Alt J
D:\Images\Concerts
```

This will store `Alt K` folder and `Concerts` folder in `D:\Temp`, ending in a structure like:
```
D
  Temp
    Current Datetime
      Alt J
      Concerts
```

usage: [-h] [--file_path FILE_PATH] [--history_level HISTORY_LEVEL]

optional arguments:

  --file_path FILE_PATH
                        Path to the file that contains information. The first line of that file, is the destiny folder
  --history_level HISTORY_LEVEL
                        Number of backups to safe before starting to delete the oldest one(s)
