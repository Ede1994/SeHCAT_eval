# Installation Guide
You have to have Python 3 with the following packages installed:

- numpy
- math
- tkinter
- os
- reportlab
- matplotlib
- pydicom

e.g.:
```
$ pip install numpy matplotlib tk reportlab pydicom
```

It's recommended to use a Python environment like Anaconda. After installation you can use Anacondas package manager ``conda`` to install the required packages.


# Windows
For convert in .exe-file: use auto-py-to-exe (or pyinstaller directly) in Prompt shell. If you want to see possible error messages, you must create a console based file. Make sure that all dependencies are up to date:
```
$ pip install --user --upgrade pip
$ pip install --user --upgrade pyinstaller
$ pip install --user --upgrade auto-py-to-exe
```
It is recommended to use pyinstaller.
```
$ pyinstaller --onedir sehcat_eval_gui_complete.py functions.py gui_functions.py
```

# Ubuntu
It is recommended to use pyinstaller.

```
$ pip install pyinstaller
$ pyinstaller --onedir sehcat_eval_gui_complete.py functions.py gui_functions.py
```
