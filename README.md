# Backuper
SimpleBackuper

It will store all folders form the list in a subfolder of the output folder with the current datetime.
The configuration is done via a json file where the output_folder must be configured. The number of backups to keep and the folders to backup. The latter can be stored in a subfolder or not, everything specified with the configuration file

Example:
conf.json content:
```
{
    "output_folder": "D:\\Backups",
    "history_level": 3,
    "folders_to_backup": [
        {
            "subfolder": "music",
            "folders": [
                "D:\\Music\\Alt J",
                "D:\\Music\\Concerts"
            ]
        },
        {
            "subfolder": "images",
            "folders": [
                "D:\\Pictures\\Holidays",
                "D:\\Pictures\\Webcam"
            ]
        },
        {
            "folders": [
                "D:\\Documents\\Expenses"
            ]
        }
    ]
}
```

This will store `Alt K` folder and `Concerts` folder in `D:\Backups`, ending in a structure like:
```
D
  Backups
    Current Datetime
      music
        Alt J
        Concerts
      images
        Holidays
        Webcam
      Expenses
```

By default, the configuration file will be searched for at the same folder as the executable with name conf.json.
usage: [-h] [--file_path FILE_PATH]

optional arguments:

  --file_path FILE_PATH
                        Path to the file that contains information. The first line of that file, is the destiny folder
