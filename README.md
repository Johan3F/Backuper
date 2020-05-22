# Backuper
SimpleBackuper

It's a simple backp program. It expect a text file where the first line is the output folder, and the next files are folder to by synced in the output folder

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
      Alt J
      Concerts
```
