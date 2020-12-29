#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright 2020

Author: Eric Einspänner, Clinic for Radiology and Nuclear Medicine, UMMD Magdeburg (Germany)

This program is free software.
"""

import tkinter as tk
from tkinter import filedialog

import os
import numpy as np

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

#%% constants and memory

decay_factor = 1.04


patdata = {'Name': 0,                     #name     
          'Birthday': 0,                  #date of birth
	      'Retention 1-Fenster [%]': 0,   #retention_1w[%]
	      'Retention 2-Fenster [%]': 0,   #retention_2w[%] 
	      'Applied Activity [MBq]': 0,    #applied activity [MBq]
	      }


#%% buttons for GUI

# delete all entries (entry boxes)
def delete_entries():
    entry_background_0d.delete(0, tk.END)
    entry_background_7d.delete(0, tk.END)
    entry_ant_counts_0d.delete(0, tk.END)
    entry_post_counts_0d.delete(0, tk.END)
    entry_ant_counts_7d.delete(0, tk.END)
    entry_post_counts_7d.delete(0, tk.END)
    
    entry_background_0d_window1.delete(0, tk.END)
    entry_background_7d_window1.delete(0, tk.END)
    entry_background_0d_window2.delete(0, tk.END)
    entry_background_7d_window2.delete(0, tk.END)
    entry_ant_counts_0d_window1.delete(0, tk.END)
    entry_post_counts_0d_window1.delete(0, tk.END)
    entry_ant_counts_7d_window1.delete(0, tk.END)
    entry_post_counts_7d_window1.delete(0, tk.END)
    entry_ant_counts_0d_window2.delete(0, tk.END)
    entry_post_counts_0d_window2.delete(0, tk.END)
    entry_ant_counts_7d_window2.delete(0, tk.END)
    entry_post_counts_7d_window2.delete(0, tk.END)


# text for help button
def helpButton():
    filewin = tk.Toplevel(root)
    filewin.title("Help")
    S = tk.Scrollbar(filewin)
    T = tk.Text(filewin, height=10, width=110)
    S.pack(side=tk.RIGHT , fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote= '''Alle Felder entsprechend ausfüllen. Beachte: Angaben in kilo-Counts [kcts]!
Durch das Betätigen des 'Berechnen!'-Buttons wird die Retention nach 7 Tagen in % ausgegeben!
1-Energiefenster: Diese Eingabemaske benutzen, wenn nur EIN Energiefenster für die WB genutzt wurde.
2-Energiefenster: Diese Eingabemaske benutzen, wenn nur ZWEI Energiefenster für die WB genutzt wurde.

English:
Please fill in all fields accordingly. Note: Data in kilo-counts!
Press the 'Berechnen!'-Button to get the final retention in %.
One energy window: Use this mask, if only one energy window was set for the WB.
Two energy windows: Use this mask, if two energy windows were set for the WB.'''
    T.insert(tk.END, quote)


# text for impressum button
def impressum():
    filewin = tk.Toplevel(root)
    filewin.title("Impressum")
    S = tk.Scrollbar(filewin)
    T = tk.Text(filewin, height=10, width=110)
    S.pack(side=tk.RIGHT , fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote= '''Author: Eric Einspänner (Clinic for Radiology and Nuclear Medicine, UMMD Magdeburg (Germany))
Contact: eric.einspaenner@med.ovgu.de
GitHub:

This program is free software.'''
    T.insert(tk.END, quote)

# save button; pdf printout
def SaveData():    
    # open dialog
    file = filedialog.asksaveasfile(title="Save As...", filetypes=[("All files", "*.*")])

    #  asksaveasfile return `None` if dialog closed with "cancel". 
    if file is None:
        return

    # extract filename as str
    filename = str(file.name)
    
    file.close()
    
    #create pdf File and define settings
    save = canvas.Canvas(filename + '.pdf', pagesize=letter)
    save.setLineWidth(.3)
    save.setFont('Helvetica', 12)

    
    # pdf header
    save.drawString(30,750, 'Universitätsmedizin Magdeburg')
    save.drawString(30,735, 'Klinik für Radiologie und Nuklearmedizin')
    save.drawString(440,750, "Datum:")
    save.line(480,747,580,747)
    
    save.drawString(30,700,'Protokoll für SeHCAT Evaluierung')
    save.line(30,698,580,698)

    # patient infos
    save.drawString(30,680, '1. Messung:')
    save.drawString(320,680, '2. Messung:')
  
    save.drawString(30,630, 'Patienteninformationen:')
    
    save.drawString(30,610, 'Name:')
    save.drawString(320,610, 'Geburtsdatum:')

    save.drawString(30,585, 'appl. Aktivität [MBq]:')
    save.drawString(320,585, 'App.-zeitpunkt:')

    save.line(30,567,580,567)
    
    # results
    save.drawString(30,550, 'Ergebnis 1-Energiefenster:')
    save.drawString(30,530, 'Retention [%]:')
    save.drawString(150,530, str(patdata['Retention 1-Fenster [%]']))

    save.drawString(350,550, 'Ergebnis 2-Energiefenster:')
    save.drawString(350,530, 'Retention [%]:')
    save.drawString(470,530, str(patdata['Retention 2-Fenster [%]']))
    
    # sgn area
    save.drawString(30,480, "Unterschrift MPE:")
    save.line(125,477,320,477)


    # save pdf file
    save.showPage()
    save.save()
    
    # remove tmp files
    os.remove(filename)


#%% calculation button for one energy window

def buttonCalculate_1():
    # get values
	# background 0d
    background_0d = entry_background_0d.get()
    if background_0d == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 0d!"
        )
    else:
	    background_0d = float(background_0d) * 10**3

	# background 7d
    background_7d = entry_background_7d.get()
    if background_7d == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 7d!"
        )
    else:
	    background_7d = float(background_7d) * 10**3

	# Ant 0d
    ant_counts_0d = entry_ant_counts_0d.get()
    if ant_counts_0d == '':
	    tk.messagebox.showerror(
            "Keine Ant counts",
            "Fehler: Keine ant counts 0d!"
        )
    else:
	    ant_counts_0d = float(ant_counts_0d) * 10**3

	# Post 0d
    post_counts_0d = entry_post_counts_0d.get()
    if post_counts_0d == '':
	    tk.messagebox.showerror(
            "Keine Post counts",
            "Fehler: Keine post counts 0d!"
        )
    else:
	    post_counts_0d = float(post_counts_0d) * 10**3

	# Ant 7d
    ant_counts_7d = entry_ant_counts_7d.get()
    if ant_counts_7d == '':
	    tk.messagebox.showerror(
            "Keine Ant counts",
            "Fehler: Keine ant counts 7d!"
        )
    else:
	    ant_counts_7d = float(ant_counts_7d) * 10**3

	# Post 7d
    post_counts_7d = entry_post_counts_7d.get()
    if post_counts_7d == '':
	    tk.messagebox.showerror(
            "Keine Post counts",
            "Fehler: Keine post counts 7d!"
        )
    else:
	    post_counts_7d = float(post_counts_7d) * 10**3

    retention_1w = round(decay_factor * (np.sqrt((ant_counts_7d - background_7d)*(post_counts_7d - background_7d))/np.sqrt((ant_counts_0d - background_0d)*(post_counts_0d - background_0d))) * 100., 2)

    # results; add in label areas
    label_areaRetention.config(text=str(retention_1w))
    patdata['Retention 1-Fenster [%]'] = retention_1w


#%% calculation button for two energy window

def buttonCalculate_2():
    # get values
	# background 0d
    background_0d_window1 = entry_background_0d_window1.get()
    if background_0d_window1 == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 0d!"
        )
    else:
	    background_0d_window1 = float(background_0d_window1) * 10**3

	# background 7d
    background_7d_window1 = entry_background_7d_window1.get()
    if background_7d_window1 == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 7d!"
        )
    else:
	    background_7d_window1 = float(background_7d_window1) * 10**3

    # window 2
    background_0d_window2 = entry_background_0d_window2.get()
    if background_0d_window2 == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 0d!"
        )
    else:
	    background_0d_window2 = float(background_0d_window2) * 10**3

	# background 7d
    background_7d_window2 = entry_background_7d_window2.get()
    if background_7d_window2 == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 7d!"
        )
    else:
	    background_7d_window2 = float(background_7d_window2) * 10**3

    # window 1
	# Ant 0d
    ant_counts_0d_window1 = entry_ant_counts_0d_window1.get()
    if ant_counts_0d_window1 == '':
	    tk.messagebox.showerror(
            "Keine Ant counts",
            "Fehler: Keine ant counts 0d für 1-Energiefenster!"
        )
    else:
	    ant_counts_0d_window1 = float(ant_counts_0d_window1) * 10**3

	# Post 0d
    post_counts_0d_window1 = entry_post_counts_0d_window1.get()
    if post_counts_0d_window1 == '':
	    tk.messagebox.showerror(
            "Keine Post counts",
            "Fehler: Keine post counts 0d für 1-Energiefenster!"
        )
    else:
	    post_counts_0d_window1 = float(post_counts_0d_window1) * 10**3

	# Ant 7d
    ant_counts_7d_window1 = entry_ant_counts_7d_window1.get()
    if ant_counts_7d_window1 == '':
	    tk.messagebox.showerror(
            "Keine Ant counts",
            "Fehler: Keine ant counts 7d für 1-Energiefenster!"
        )
    else:
	    ant_counts_7d_window1 = float(ant_counts_7d_window1) * 10**3

	# Post 7d
    post_counts_7d_window1 = entry_post_counts_7d_window1.get()
    if post_counts_7d_window1 == '':
	    tk.messagebox.showerror(
            "Keine Post counts",
            "Fehler: Keine post counts 7d für 1-Energiefenster!"
        )
    else:
	    post_counts_7d_window1 = float(post_counts_7d_window1) * 10**3

    # window 2
	# Ant 0d
    ant_counts_0d_window2 = entry_ant_counts_0d_window2.get()
    if ant_counts_0d_window2 == '':
	    tk.messagebox.showerror(
            "Keine Ant counts",
            "Fehler: Keine ant counts 0d für 2-Energiefenster!"
        )
    else:
	    ant_counts_0d_window2 = float(ant_counts_0d_window2) * 10**3

	# Post 0d
    post_counts_0d_window2 = entry_post_counts_0d_window2.get()
    if post_counts_0d_window2 == '':
	    tk.messagebox.showerror(
            "Keine Post counts",
            "Fehler: Keine post counts 0d für 2-Energiefenster!"
        )
    else:
	    post_counts_0d_window2 = float(post_counts_0d_window2) * 10**3

	# Ant 7d
    ant_counts_7d_window2 = entry_ant_counts_7d_window2.get()
    if ant_counts_7d_window2 == '':
	    tk.messagebox.showerror(
            "Keine Ant counts",
            "Fehler: Keine ant counts 7d für 2-Energiefenster!"
        )
    else:
	    ant_counts_7d_window2 = float(ant_counts_7d_window2) * 10**3

	# Post 7d
    post_counts_7d_window2 = entry_post_counts_7d_window2.get()
    if post_counts_7d_window2 == '':
	    tk.messagebox.showerror(
            "Keine Post counts",
            "Fehler: Keine post counts 7d für 2-Energiefenster!"
        )
    else:
	    post_counts_7d_window2 = float(post_counts_7d_window2) * 10**3

    # retention = (window1 + window2)/2 (round -> .00)
    retention_2w = round(decay_factor * (np.sqrt((ant_counts_7d_window1 + ant_counts_7d_window2 - background_7d_window1 - background_7d_window2)*(post_counts_7d_window1 + post_counts_7d_window2 - background_7d_window1 - background_7d_window2))) \
                      / np.sqrt((ant_counts_0d_window1 + ant_counts_0d_window2 - background_0d_window1 - background_7d_window2)*(post_counts_0d_window1 + post_counts_7d_window2 - background_0d_window1 - background_7d_window2)) * 100., 2)
    
    # results; add in label areas
    label_areaRetention_2.config(text=str(retention_2w))
    patdata['Retention 2-Fenster [%]'] = retention_2w


#%% GUI
# start GUI
root = tk.Tk()
root.title("SeHCAT - Auswertung")
root.geometry("710x550")

# define menu
menubar = tk.Menu(root)

# file menu
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Speichern als...", command=SaveData)
filemenu.add_separator()
filemenu.add_command(label="Verlassen", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# edit menu
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Alles löschen", command=delete_entries)
menubar.add_cascade(label="Bearbeiten", menu=editmenu)

# help menu
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Hilfe", command=helpButton)
helpmenu.add_command(label="Impressum", command=impressum)
menubar.add_cascade(label="Hilfe", menu=helpmenu)

root.config(menu=menubar)


#%% one energy window
group_1 = tk.LabelFrame(root, padx=15, pady=10, text="1-Energiefenster")
group_1.grid(padx=10, pady=5, sticky='w' + 'e')

# background
label_background_0d = tk.Label(group_1, text="Hintergrund 0d [kcts]:").grid(row=0)
label_background_7d = tk.Label(group_1, text="Hintergrund 7d [kcts]:").grid(row=0, column=3)

entry_background_0d = tk.Entry(group_1)
entry_background_0d.grid(row=0, column=1)

entry_background_7d = tk.Entry(group_1)
entry_background_7d.grid(row=0, column=4)

# 0 days
label_ant_counts_0d = tk.Label(group_1, text="Ant 0d [kcts]:").grid(row=1)
label_post_counts_0d = tk.Label(group_1, text="Post 0d [kcts]:").grid(row=1, column=3)

entry_ant_counts_0d = tk.Entry(group_1)
entry_ant_counts_0d.grid(row=1, column=1)

entry_post_counts_0d = tk.Entry(group_1)
entry_post_counts_0d.grid(row=1, column=4)

# 7 days
label_ant_counts_7d = tk.Label(group_1, text="Ant 7d [kcts]:").grid(row=2)
label_post_counts_7d = tk.Label(group_1, text="Post 7d [kcts]:").grid(row=2, column=3)

entry_ant_counts_7d = tk.Entry(group_1)
entry_ant_counts_7d.grid(row=2, column=1)

entry_post_counts_7d = tk.Entry(group_1)
entry_post_counts_7d.grid(row=2, column=4)

# retention
label_retention = tk.Label(group_1, text="Tag 7 Retention [%]:").grid(row=4)
label_areaRetention = tk.Label(group_1, bg='gray', width='12', text="")
label_areaRetention.grid(row=4, column=1)

# define button position
buttonCalculate = tk.Button(group_1, text='Berechnen!', width='10', bg='red', command=buttonCalculate_1)
buttonCalculate.grid(row=4, column=4, padx='5', pady='5')


#%% two energy windows
group_2 = tk.LabelFrame(root, padx=15, pady=10, text="2-Energiefenster")
group_2.grid(padx=10, pady=5, sticky='w' + 'e')

# background
group_2b = tk.LabelFrame(group_2, padx=15, pady=10, text="Hintergrund")
group_2b.grid(padx=10, pady=5, sticky='w' + 'e')

label_background_0d_window1 = tk.Label(group_2b, text="Hintergrund 0d [kcts]:").grid(row=0)
label_background_7d_window1 = tk.Label(group_2b, text="Hintergrund 7d [kcts]:").grid(row=0, column=3)

entry_background_0d_window1 = tk.Entry(group_2b)
entry_background_0d_window1.grid(row=0, column=1)

entry_background_7d_window1 = tk.Entry(group_2b)
entry_background_7d_window1.grid(row=0, column=4)

label_background_0d_window2 = tk.Label(group_2b, text="Hintergrund 0d [kcts]:").grid(row=1)
label_background_7d_window2 = tk.Label(group_2b, text="Hintergrund 7d [kcts]:").grid(row=1, column=3)

entry_background_0d_window2 = tk.Entry(group_2b)
entry_background_0d_window2.grid(row=1, column=1)

entry_background_7d_window2 = tk.Entry(group_2b)
entry_background_7d_window2.grid(row=1, column=4)

# energy window 1
group_21 = tk.LabelFrame(group_2, padx=15, pady=10, text="1. Energiefenster")
group_21.grid(padx=10, pady=5, sticky='w' + 'e')

label_ant_counts_0d_window1 = tk.Label(group_21, text="Ant 0d [kcts]:").grid(row=1)
label_post_counts_0d_window1 = tk.Label(group_21, text="Post 0d [kcts]:").grid(row=1, column=3, padx=26)

label_ant_counts_7d_window1 = tk.Label(group_21, text="Ant 7d [kcts]:").grid(row=2)
label_post_counts_7d_window1 = tk.Label(group_21, text="Post 7d [kcts]:").grid(row=2, column=3, padx=26)

entry_ant_counts_0d_window1 = tk.Entry(group_21)
entry_ant_counts_0d_window1.grid(row=1, column=1, padx=10)

entry_post_counts_0d_window1 = tk.Entry(group_21)
entry_post_counts_0d_window1.grid(row=1, column=4, padx=15)

entry_ant_counts_7d_window1 = tk.Entry(group_21)
entry_ant_counts_7d_window1.grid(row=2, column=1, padx=10)

entry_post_counts_7d_window1 = tk.Entry(group_21)
entry_post_counts_7d_window1.grid(row=2, column=4, padx=15)

# energy window 2
group_22 = tk.LabelFrame(group_2, padx=15, pady=10, text="2. Energiefenster")
group_22.grid(padx=10, pady=5, sticky='w' + 'e')

label_ant_counts_0d_window2 = tk.Label(group_22, text="Ant 0d [kcts]:").grid(row=1)
label_post_counts_0d_window2 = tk.Label(group_22, text="Post 0d [kcts]:").grid(row=1, column=3, padx=26)

label_ant_counts_7d_window2 = tk.Label(group_22, text="Ant 7d [kcts]:").grid(row=2)
label_post_counts_7d_window2 = tk.Label(group_22, text="Post 7d [kcts]:").grid(row=2, column=3, padx=26)

entry_ant_counts_0d_window2 = tk.Entry(group_22)
entry_ant_counts_0d_window2.grid(row=1, column=1, padx=10)

entry_post_counts_0d_window2 = tk.Entry(group_22)
entry_post_counts_0d_window2.grid(row=1, column=4, padx=15)

entry_ant_counts_7d_window2 = tk.Entry(group_22)
entry_ant_counts_7d_window2.grid(row=2, column=1, padx=10)

entry_post_counts_7d_window2 = tk.Entry(group_22)
entry_post_counts_7d_window2.grid(row=2, column=4, padx=15)

# retention
group_2r = tk.LabelFrame(group_2, padx=15, pady=10, text="Retention")
group_2r.grid(padx=10, pady=5, sticky='w' + 'e')

label_retention_2 = tk.Label(group_2r, text="Tag 7 Retention [%]:").grid(row=4)
label_areaRetention_2 = tk.Label(group_2r, bg='gray', width='12', text="")
label_areaRetention_2.grid(row=4, column=1, padx=10)

# define button position
buttonCalculate_2 = tk.Button(group_2r, text='Berechnen!', width='10', bg='red', command=buttonCalculate_2)
buttonCalculate_2.grid(row=4, column=3, padx=150, pady=5)


#%% main
root.mainloop()