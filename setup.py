# -*- coding: utf-8 -*-
"""
configuration
"""
import cx_Freeze
import sys
import os
from shutil import copy

# Dependencies are automatically detected, but it might need fine tuning
build_exe_options = {"packages":["tkinter","matplotlib", "os", "numpy", "math", "pydicom", "io", "datetime","reportlab"],
                     "excludes":["scipy"],
                     "include_files":["gui_functions.py", "functions.py","nuclear.ico"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("sehcat_eval_gui_complete.py",
                                    base=base,
                                    target_name="SeHCAT.exe",
                                    shortcut_name="SeHCAT",
                                    icon="nuclear.ico")]

cx_Freeze.setup(
    name = "SeHCAT",
    version = "1.0",
    description = "SeHCAT Evaluation Program",
    author = 'Eric Einspänner, Clinic for Radiology and Nuclear Medicine, UMMD Magdeburg (Germany)',
    options = {"build_exe": build_exe_options},    
    executables = executables
    )


# copy necessary .dll files to correct dir
build_dir = os.path.join('build/exe.win-amd64-3.8')
numpy_mkl_dir = os.path.join('build/exe.win-amd64-3.8', 'lib', 'numpy_mkl')
for file_name in os.listdir(numpy_mkl_dir):
    if file_name.startswith('mkl'):
        file_path = os.path.join(numpy_mkl_dir, file_name)
        copy(file_path, build_dir)
        print('Copy: ', file_name)

    if file_name == 'libiomp5md.dll':
        file_path = os.path.join(numpy_mkl_dir, file_name)
        copy(file_path, build_dir)
        print('Copy: ', file_name)
