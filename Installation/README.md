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

Alternative:
Use `cx_freezer` for the creation of the build or a installation dist. You can find the example `setup.py` in the main folder.
```
python setup.py build
or
python setup.py bdist_msi
```
It is recommended to use a virtual environment with just the necessary packages.


# Troubleshooting
If the application doesn't start, then it is recommended to run the bash file `start.bat` so that the error message appears in the console.

# Ubuntu
It is recommended to use pyinstaller.

```
$ pip install pyinstaller
$ pyinstaller --onedir sehcat_eval_gui_complete.py functions.py gui_functions.py
```
