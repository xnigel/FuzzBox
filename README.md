# FuzzBox demo
<img src="https://github.com/xnigel/FuzzBox/blob/main/demo/FuzzBox%20demo%201.png" width =250> <img src="https://github.com/xnigel/FuzzBox/blob/main/demo/FuzzBox%20demo%202.png" width =250>

## Execute the *.exe file
Simply download the FuzzBox.exe executable file from "dist" folder and execute it from your local drive.

## Convert *.py file to *.exe file
When you are going to modify the original py file and convert it into exe format executable, you may need to perform the following commands.
```
sudo apt-get install pyinstaller
```

Then go to the *.py directory:
```
pyinstaller.exe --onefile --windowed --icon=xxx.ico xxx.py
```