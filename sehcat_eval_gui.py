#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright 2020

Author: Eric Einspänner, Clinic for Radiology and Nuclear Medicine, UMMD Magdeburg (Germany)

This program is free software.
"""

import tkinter as tk
from tkinter import ttk

import numpy as np

#%% constants

decay_factor = 1.04

#%% buttons for GUI
# functions: GUI

# do nothing button
def donothing():
    filewin = tk.Toplevel(root)
    button = tk.Button(filewin,
                       text="Do nothing button"
                       )
    button.pack()


# delete all entries (entry boxes)
def delete_entries():
    entry_background_0d.delete(0, tk.END)
    entry_background_7d.delete(0, tk.END)
    entry_ant_counts_0d.delete(0, tk.END)
    entry_post_counts_0d.delete(0, tk.END)
    entry_ant_counts_7d.delete(0, tk.END)
    entry_post_counts_7d.delete(0, tk.END)
    
    entry_background_0d_2.delete(0, tk.END)
    entry_background_7d_2.delete(0, tk.END)
    entry_ant_counts_0d_2.delete(0, tk.END)
    entry_post_counts_0d_2.delete(0, tk.END)
    entry_ant_counts_7d_2.delete(0, tk.END)
    entry_post_counts_7d_2.delete(0, tk.END)


# text for impressum button
def helpButton():
    filewin = tk.Toplevel(root)
    filewin.title("Help")
    S = tk.Scrollbar(filewin)
    T = tk.Text(filewin, height=10, width=100)
    S.pack(side=tk.RIGHT , fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote= '''Please fill in all fields accordingly. Note: Data in kilo-counts!
Press the 'Calculate!'-Button to get the final retention in %.

One energy window: Use this mask, if only one energy window was set for the WB.
Two energy windows: Use this mask, if two energy windows were set for the WB.'''
    T.insert(tk.END, quote)


# text for impressum button
def impressum():
    filewin = tk.Toplevel(root)
    filewin.title("Impressum")
    S = tk.Scrollbar(filewin)
    T = tk.Text(filewin, height=10, width=100)
    S.pack(side=tk.RIGHT , fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote= '''Author: Eric Einspänner (Clinic for Radiology and Nuclear Medicine, UMMD Magdeburg (Germany))
This program is free software.
eric.einspaenner@med.ovgu.de'''
    T.insert(tk.END, quote)


# calculation button for one energy window
def buttonCalculate_1():
    # get the values

	# background 0d
    background_0d = entry_background_0d.get()
    if background_0d == '':
	    tk.messagebox.showerror(
            "Missing Background",
            "Error: No background 0d!"
        )
    else:
	    background_0d = float(background_0d) * 10**3

	# background 7d
    background_7d = entry_background_7d.get()
    if background_7d == '':
	    tk.messagebox.showerror(
            "Missing Background",
            "Error: No background 7d!"
        )
    else:
	    background_7d = float(background_7d) * 10**3

	# Ant 0d
    ant_counts_0d = entry_ant_counts_0d.get()
    if ant_counts_0d == '':
	    tk.messagebox.showerror(
            "Missing Ant counts",
            "Error: No ant counts 0d!"
        )
    else:
	    ant_counts_0d = float(ant_counts_0d) * 10**3

	# Post 0d
    post_counts_0d = entry_post_counts_0d.get()
    if post_counts_0d == '':
	    tk.messagebox.showerror(
            "Missing Post counts",
            "Error: No post counts 0d!"
        )
    else:
	    post_counts_0d = float(post_counts_0d) * 10**3

	# Ant 7d
    ant_counts_7d = entry_ant_counts_7d.get()
    if ant_counts_7d == '':
	    tk.messagebox.showerror(
            "Missing Ant counts",
            "Error: No ant counts 7d!"
        )
    else:
	    ant_counts_7d = float(ant_counts_7d) * 10**3

	# Post 7d
    post_counts_7d = entry_post_counts_7d.get()
    if post_counts_7d == '':
	    tk.messagebox.showerror(
            "Missing Post counts",
            "Error: No post counts 7d!"
        )
    else:
	    post_counts_7d = float(post_counts_7d) * 10**3

    retention = round(decay_factor * (np.sqrt((ant_counts_7d - background_7d)*(post_counts_7d - background_7d))/np.sqrt((ant_counts_0d - background_0d)*(post_counts_0d - background_0d))) * 100., 2)

    # results; add in label areas
    label_areaRetention.config(text=str(retention))


# calculation button for two energy window
def buttonCalculate_2():
    # get the values

	# background 0d
    background_0d = entry_background_0d_2.get()
    if background_0d == '':
	    tk.messagebox.showerror(
            "Missing Background",
            "Error: No background 0d!"
        )
    else:
	    background_0d = float(background_0d) * 10**3

	# background 7d
    background_7d = entry_background_7d_2.get()
    if background_7d == '':
	    tk.messagebox.showerror(
            "Missing Background",
            "Error: No background 7d!"
        )
    else:
	    background_7d = float(background_7d) * 10**3

	# Ant 0d
    ant_counts_0d = entry_ant_counts_0d_2.get()
    if ant_counts_0d == '':
	    tk.messagebox.showerror(
            "Missing Ant counts",
            "Error: No ant counts 0d!"
        )
    else:
	    ant_counts_0d = float(ant_counts_0d) * 10**3

	# Post 0d
    post_counts_0d = entry_post_counts_0d_2.get()
    if post_counts_0d == '':
	    tk.messagebox.showerror(
            "Missing Post counts",
            "Error: No post counts 0d!"
        )
    else:
	    post_counts_0d = float(post_counts_0d) * 10**3

	# Ant 7d
    ant_counts_7d = entry_ant_counts_7d_2.get()
    if ant_counts_7d == '':
	    tk.messagebox.showerror(
            "Missing Ant counts",
            "Error: No ant counts 7d!"
        )
    else:
	    ant_counts_7d = float(ant_counts_7d) * 10**3

	# Post 7d
    post_counts_7d = entry_post_counts_7d_2.get()
    if post_counts_7d == '':
	    tk.messagebox.showerror(
            "Missing Post counts",
            "Error: No post counts 7d!"
        )
    else:
	    post_counts_7d = float(post_counts_7d) * 10**3

    retention = round(decay_factor * (np.sqrt((ant_counts_7d - background_7d)*(post_counts_7d - background_7d))/np.sqrt((ant_counts_0d - background_0d)*(post_counts_0d - background_0d))) * 100., 2)

    # results; add in label areas
    label_areaRetention_2.config(text=str(retention))


#%% GUI
# start GUI
root = tk.Tk()
root.title("SeHCAT")
root.geometry("800x400")

# define menu
menubar = tk.Menu(root)

# file menu
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# edit menu
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Delete All", command=delete_entries)
menubar.add_cascade(label="Edit", menu=editmenu)

# help menu
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=helpButton)
helpmenu.add_command(label="Impressum", command=impressum)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)


#%% two energy windows
group_1 = tk.LabelFrame(root, padx=15, pady=10, text="One energy window")
group_1.grid(padx=10, pady=5)

label_background_0d = tk.Label(group_1, text="Background 0d in kcounts:").grid(row=0)
label_background_7d = tk.Label(group_1, text="Background 7d in kcounts:").grid(row=0, column=3)
label_ant_counts_0d = tk.Label(group_1, text="Ant 0d in kcounts:").grid(row=1)
label_post_counts_0d = tk.Label(group_1, text="Post 0d in kcounts:").grid(row=1, column=3)
label_ant_counts_7d = tk.Label(group_1, text="Ant 7d in kcounts:").grid(row=2)
label_post_counts_7d = tk.Label(group_1, text="Post 7d in kcounts:").grid(row=2, column=3)

label_retention = tk.Label(group_1, text="Day 7 Retention [%]:").grid(row=4)
label_areaRetention = tk.Label(group_1, bg='gray', width='12', text="")
label_areaRetention.grid(row=4, column=1)

entry_background_0d = tk.Entry(group_1)
entry_background_0d.grid(row=0, column=1)

entry_background_7d = tk.Entry(group_1)
entry_background_7d.grid(row=0, column=4)

entry_ant_counts_0d = tk.Entry(group_1)
entry_ant_counts_0d.grid(row=1, column=1)

entry_post_counts_0d = tk.Entry(group_1)
entry_post_counts_0d.grid(row=1, column=4)

entry_ant_counts_7d = tk.Entry(group_1)
entry_ant_counts_7d.grid(row=2, column=1)

entry_post_counts_7d = tk.Entry(group_1)
entry_post_counts_7d.grid(row=2, column=4)

# define button position
buttonCalculate = tk.Button(group_1, text='Calculate!', width='10', bg='red', command=buttonCalculate_1)
buttonCalculate.grid(row=3, column=5, padx='5', pady='5')


#%% two energy windows
group_2 = tk.LabelFrame(root, padx=15, pady=10, text="Two energy windows")
group_2.grid(padx=10, pady=5)

label_background_0d_2 = tk.Label(group_2, text="Background 0d in kcounts:").grid(row=0)
label_background_7d_2 = tk.Label(group_2, text="Background 7d in kcounts:").grid(row=0, column=3)
label_ant_counts_0d_2 = tk.Label(group_2, text="Ant 0d in kcounts:").grid(row=1)
label_post_counts_0d_2 = tk.Label(group_2, text="Post 0d in kcounts:").grid(row=1, column=3)
label_ant_counts_7d_2 = tk.Label(group_2, text="Ant 7d in kcounts:").grid(row=2)
label_post_counts_7d_2 = tk.Label(group_2, text="Post 7d in kcounts:").grid(row=2, column=3)

label_retention_2 = tk.Label(group_2, text="Day 7 Retention [%]:").grid(row=4)
label_areaRetention_2 = tk.Label(group_2, bg='gray', width='12', text="")
label_areaRetention_2.grid(row=4, column=1)

entry_background_0d_2 = tk.Entry(group_2)
entry_background_0d_2.grid(row=0, column=1)

entry_background_7d_2 = tk.Entry(group_2)
entry_background_7d_2.grid(row=0, column=4)

entry_ant_counts_0d_2 = tk.Entry(group_2)
entry_ant_counts_0d_2.grid(row=1, column=1)

entry_post_counts_0d_2 = tk.Entry(group_2)
entry_post_counts_0d_2.grid(row=1, column=4)

entry_ant_counts_7d_2 = tk.Entry(group_2)
entry_ant_counts_7d_2.grid(row=2, column=1)

entry_post_counts_7d_2 = tk.Entry(group_2)
entry_post_counts_7d_2.grid(row=2, column=4)

# define button position
buttonCalculate_2 = tk.Button(group_2, text='Calculate!', width='10', bg='red', command=buttonCalculate_2)
buttonCalculate_2.grid(row=3, column=5, padx='5', pady='5')


#%% main
root.mainloop()