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
import math

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#%% constants and memory

decay_factor = 1.04
T_75se = 118. # days

# storage for patient data
patdata = {'Name': "-", 
          'Birthday': "-",
          'Weight':"-",
          'Height': "-",
	      'Applied Activity [kBq]': "-",
          'Application Date': "-",
	      'Retention 1-Fenster [%]': "-",
	      'Retention 2-Fenster [%]': "-",
          '1st Measurement': "-",
          '2nd Measurement': "-"
	      }

# define figures for GUI
fig = Figure(figsize=(4, 6), dpi=60)
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

# describe the physical decay of radioactivity
def decay_equation(a0,T,t):
	# A = A0 * e^(- λ * t)
	a = int(a0 * math.exp(-math.log(2)/T * t))
	return a

# calculate physical decay of Se-75
def selen_decay(counts_0d):
    dt = 0.0
    dt_list = []
    decay =  []
    while dt <= 8.0:
        x = decay_equation(counts_0d, T_75se, dt)
        decay.append(x)
        dt_list.append(dt)
        dt += 0.1
    return dt_list, decay

# calculate 10% and 15% retentions curve
def retention_lists(counts_0d):
    retention_10 = []
    retention_15 = []
    dt = 0.0
    dt_list = []
    factor1 = 1.
    factor2 = 1.
    while dt <= 8.0:
        x = decay_equation(counts_0d, T_75se, dt)*factor1
        factor1 -= factor1*0.15
        y = decay_equation(counts_0d, T_75se, dt)*factor2
        factor2 -= factor2*0.125
        retention_10.append(x)
        retention_15.append(y)
        dt_list.append(dt)
        dt += 0.5
    return dt_list, retention_10, retention_15


#%% buttons for GUI

# delete all entries (entry boxes)
def delete_entries():
    entry_background_0d_ant.delete(0, tk.END)
    entry_background_7d_ant.delete(0, tk.END)
    entry_background_0d_post.delete(0, tk.END)
    entry_background_7d_post.delete(0, tk.END)
    entry_ant_counts_0d.delete(0, tk.END)
    entry_post_counts_0d.delete(0, tk.END)
    entry_ant_counts_7d.delete(0, tk.END)
    entry_post_counts_7d.delete(0, tk.END)
    
    entry_background_0d_ant_w1.delete(0, tk.END)
    entry_background_0d_post_w1.delete(0, tk.END)
    entry_background_7d_ant_w1.delete(0, tk.END)
    entry_background_7d_post_w1.delete(0, tk.END)
    entry_background_0d_ant_w2.delete(0, tk.END)
    entry_background_0d_post_w2.delete(0, tk.END)
    entry_background_7d_ant_w2.delete(0, tk.END)
    entry_background_7d_post_w2.delete(0, tk.END)
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
    quote= '''Alle Felder entsprechend ausfüllen. Achtung: Angaben in kilo-Counts [kcts]!
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
    
    patdata['Name'] = entry_patname.get()
    patdata['Birthday'] = entry_patbirth.get()
    patdata['Height'] = entry_patheight.get()
    patdata['Weight'] = entry_patweight.get()
    patdata['Applied Activity [kBq]'] = entry_patactivity.get()
    patdata['Application Date'] = entry_patactdate.get()
    patdata['1st Measurement'] = entry_pat_date_1st.get()
    patdata['2nd Measurement'] = entry_pat_date_2nd.get()
    
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
    save.drawString(100,680, str(patdata['1st Measurement']))
    save.drawString(320,680, '2. Messung:')
    save.drawString(390,680, str(patdata['2nd Measurement']))
  
    save.drawString(30,630, 'Patienteninformationen:')
    
    save.drawString(30,610, 'Name:')
    save.drawString(100,610, str(patdata['Name']))
    save.drawString(320,610, 'Geburtsdatum:')
    save.drawString(420,610, str(patdata['Birthday']))
    
    save.drawString(30,590, 'Größe [cm]:')
    save.drawString(100,590, str(patdata['Height']))
    save.drawString(320,590, 'Gewicht [kg]:')
    save.drawString(420,590, str(patdata['Weight']))

    save.drawString(30,565, 'appl. Aktivität [kBq]:')
    save.drawString(150,565, str(patdata['Applied Activity [kBq]']))
    save.drawString(320,565, 'App.-zeitpunkt:')
    save.drawString(420,565, str(patdata['Application Date']))

    save.line(30,547,580,547)
    
    # results
    save.drawString(30,530, 'Ergebnis 1-Energiefenster:')
    save.drawString(30,510, 'Retention [%]:')
    save.drawString(150,510, str(patdata['Retention 1-Fenster [%]']))

    save.drawString(350,530, 'Ergebnis 2-Energiefenster:')
    save.drawString(350,510, 'Retention [%]:')
    save.drawString(470,510, str(patdata['Retention 2-Fenster [%]']))
    
    # sgn area
    save.drawString(30,460, "Unterschrift MPE:")
    save.line(125,457,320,457)


    # save pdf file
    save.showPage()
    save.save()
    
    # remove tmp files
    os.remove(filename)


#%% calculation button for one energy window

def buttonCalculate_1():
    # get values
	# background ant 0d
    background_0d_ant = entry_background_0d_ant.get()
    if background_0d_ant == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 0d!"
        )
    else:
	    background_0d_ant = float(background_0d_ant) * 10**3

	# background ant 7d
    background_7d_ant = entry_background_7d_ant.get()
    if background_7d_ant == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 7d!"
        )
    else:
	    background_7d_ant = float(background_7d_ant) * 10**3

	# background post 0d
    background_0d_post = entry_background_0d_post.get()
    if background_0d_post == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 0d!"
        )
    else:
	    background_0d_post = float(background_0d_post) * 10**3

	# background post 7d
    background_7d_post = entry_background_7d_post.get()
    if background_7d_post == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 7d!"
        )
    else:
	    background_7d_post = float(background_7d_post) * 10**3

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

    retention_1w = round(decay_factor * (np.sqrt((ant_counts_7d - background_7d_ant)*(post_counts_7d - background_7d_post)) \
                                         / np.sqrt((ant_counts_0d - background_0d_ant)*(post_counts_0d - background_0d_post))) * 100., 2)
    
    counts_0d = ((ant_counts_0d - background_0d_ant) + (post_counts_0d - background_0d_post)) / 2.
    counts_7d = ((ant_counts_7d - background_7d_ant)  + (post_counts_7d - background_7d_post)) / 2.
    
    dt_list, retention_10, retention_15 = retention_lists(counts_0d)
    dt_selen, decay_selen = selen_decay(counts_0d)

    # results; add in label areas
    label_areaRetention_1.config(text=str(retention_1w))
    patdata['Retention 1-Fenster [%]'] = retention_1w
    
    # plot
    ax1.clear()
    ax2.clear()
    
    #ax1.set_title('kcts vs Tagen')
    ax1.plot(0, counts_0d, 'o', label='kcts 0d')
    ax1.plot(7, counts_7d, 'o', label='kcts 7d')
    ax1.plot(dt_selen, decay_selen, label='physikalischer Zerfall Se-75')
    ax1.axvline(x = 0, color='red', linestyle='--', linewidth='0.33')
    ax1.axvline(x = 7, color='red', linestyle='--', linewidth='0.33')
    ax1.set_ylabel('kcts')
    ax1.set_xlabel('Tagen')
    ax1.legend()
    
    ax2.plot(dt_list, retention_10, label='Retention = 10%')
    ax2.plot(dt_list, retention_15, label='Retention = 15%')
    ax2.plot(7., counts_7d, 'o')
    ax2.annotate('Retention',
            xy=(dt_list[-3], retention_1w),
            )
    ax2.axvline(x = 0, color='red', linestyle='--', linewidth='0.33')
    ax2.axvline(x = 7, color='red', linestyle='--', linewidth='0.33')
    ax2.set_ylabel('kcts')
    ax2.set_xlabel('Tagen')
    ax2.legend()
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=2, rowspan=2, columnspan=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=1, pady=1)
    
    toolbarFrame = tk.Frame(master=root)
    toolbarFrame.grid(row=3, column=2, columnspan=3)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)


#%% calculation button for two energy window

def buttonCalculate_2():
    # get values
	# background ant 0d w2
    background_0d_ant_w1 = entry_background_0d_ant_w1.get()
    if background_0d_ant_w1 == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 0d!"
        )
    else:
	    background_0d_ant_w1 = float(background_0d_ant_w1) * 10**3

	# background 0d post w2
    background_0d_post_w1 = entry_background_0d_post_w1.get()
    if background_0d_post_w1 == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 7d!"
        )
    else:
	    background_0d_post_w1 = float(background_0d_post_w1) * 10**3

    # background ant 7d w2
    background_7d_ant_w1 = entry_background_7d_ant_w1.get()
    if background_7d_ant_w1 == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 0d!"
        )
    else:
	    background_7d_ant_w1 = float(background_7d_ant_w1) * 10**3

	# background post 7d w2
    background_7d_post_w1 = entry_background_7d_post_w1.get()
    if background_7d_post_w1 == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 7d!"
        )
    else:
	    background_7d_post_w1 = float(background_7d_post_w1) * 10**3

    # backgound ant 0d w2
    background_0d_ant_w2 = entry_background_0d_ant_w2.get()
    if background_0d_ant_w2 == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 0d!"
        )
    else:
	    background_0d_ant_w2 = float(background_0d_ant_w2) * 10**3

	# background 0d post w2
    background_0d_post_w2 = entry_background_0d_post_w2.get()
    if background_0d_post_w2 == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 7d!"
        )
    else:
	    background_0d_post_w2 = float(background_0d_post_w2) * 10**3

    # background ant 7d w2
    background_7d_ant_w2 = entry_background_7d_ant_w2.get()
    if background_7d_ant_w2 == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 0d!"
        )
    else:
	    background_7d_ant_w2 = float(background_7d_ant_w2) * 10**3

	# background post 7d w2
    background_7d_post_w2 = entry_background_7d_post_w2.get()
    if background_7d_post_w2 == '':
	    tk.messagebox.showerror(
            "Kein Hintergrund",
            "Fehler: Kein Hintergrund 7d!"
        )
    else:
	    background_7d_post_w2 = float(background_7d_post_w2) * 10**3

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
    retention_2w = round(decay_factor * (np.sqrt((ant_counts_7d_window1 + ant_counts_7d_window2 - background_7d_ant_w1 - background_7d_ant_w2)*(post_counts_7d_window1 + post_counts_7d_window2 - background_7d_post_w1 - background_7d_post_w2))) \
                      / np.sqrt((ant_counts_0d_window1 + ant_counts_0d_window2 - background_0d_ant_w1 - background_0d_ant_w2)*(post_counts_0d_window1 + post_counts_0d_window2 - background_0d_post_w1 - background_0d_post_w2)) * 100., 2)

    counts_0d = ((ant_counts_0d_window1 + ant_counts_0d_window2 - background_0d_ant_w1 - background_0d_ant_w2) + (post_counts_0d_window1 + post_counts_0d_window2 - background_0d_post_w1 - background_0d_post_w2)) / 2.
    counts_7d = ((ant_counts_7d_window1 + ant_counts_7d_window2 - background_7d_ant_w1 - background_7d_ant_w2) + (post_counts_7d_window1 + post_counts_7d_window2 - background_7d_post_w1 - background_7d_post_w2)) / 2.
        
    # results; add in label areas
    label_areaRetention_2.config(text=str(retention_2w))
    patdata['Retention 2-Fenster [%]'] = retention_2w
    
    dt_list, retention_10, retention_15 = retention_lists(counts_0d)
    dt_selen, decay_selen = selen_decay(counts_0d)

    # plot
    ax1.clear()
    ax2.clear()
    
    #ax1.set_title('kcts vs Tagen')
    ax1.plot(0, counts_0d, 'o', label='kcts 0d')
    ax1.plot(7, counts_7d, 'o', label='kcts 7d')
    ax1.plot(dt_selen, decay_selen, label='physikalischer Zerfall Se-75')
    ax1.axvline(x = 0, color='red', linestyle='--', linewidth='0.33')
    ax1.axvline(x = 7, color='red', linestyle='--', linewidth='0.33')
    ax1.set_ylabel('kcts')
    ax1.set_xlabel('Tagen')
    ax1.legend()
    
    ax2.plot(dt_list, retention_10, label='Retention = 10%')
    ax2.plot(dt_list, retention_15, label='Retention = 15%')
    ax2.plot(7., counts_7d, 'o')
    ax2.annotate('Retention',
            xy=(dt_list[-3], retention_2w),
            )
    ax2.axvline(x = 0, color='red', linestyle='--', linewidth='0.33')
    ax2.axvline(x = 7, color='red', linestyle='--', linewidth='0.33')
    ax2.set_ylabel('kcts')
    ax2.set_xlabel('Tagen')
    ax2.legend()
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=2, rowspan=2, columnspan=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=1, pady=1)
    
    toolbarFrame = tk.Frame(master=root)
    toolbarFrame.grid(row=3, column=2, columnspan=3)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)


#%% GUI
# start GUI
root = tk.Tk()
root.title("SeHCAT - Auswertung")
root.geometry("1920x1200")

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


#%% patient data
# positions

group_patient = tk.LabelFrame(root, padx=15, pady=10, text="Patientendaten")
group_patient.grid(row=0, column=0, padx=10, pady=5, sticky='w' + 'e')

label_patname = tk.Label(group_patient, text="Name:").grid(row=0)
entry_patname = tk.Entry(group_patient)
entry_patname.grid(row=0, column=1, padx=15)

label_patbirth = tk.Label(group_patient, text="Geburtsdatum:").grid(row=1)
entry_patbirth = tk.Entry(group_patient)
entry_patbirth.grid(row=1, column=1, padx=15)

label_patheight = tk.Label(group_patient, text="Größe [cm]:").grid(row=2)
entry_patheight = tk.Entry(group_patient)
entry_patheight.grid(row=2, column=1, padx=15)

label_patweight = tk.Label(group_patient, text="Gewicht [kg]:").grid(row=3)
entry_patweight = tk.Entry(group_patient)
entry_patweight.grid(row=3, column=1, padx=15)

label_patactivity = tk.Label(group_patient, text="appl. Aktivität [kBq]:").grid(row=4)
entry_patactivity = tk.Entry(group_patient)
entry_patactivity.grid(row=4, column=1, padx=15)

label_patactdate = tk.Label(group_patient, text="App.-zeitpunkt:").grid(row=5)
entry_patactdate = tk.Entry(group_patient)
entry_patactdate.grid(row=5, column=1, padx=15)

label_pat_date_1st = tk.Label(group_patient, text="1. Messung:").grid(row=6)
entry_pat_date_1st = tk.Entry(group_patient)
entry_pat_date_1st.grid(row=6, column=1, padx=15)

label_pat_date_2nd = tk.Label(group_patient, text="2. Messung:").grid(row=7)
entry_pat_date_2nd = tk.Entry(group_patient)
entry_pat_date_2nd.grid(row=7, column=1, padx=15)

#%% plot area
# position
plot_frame = tk.Frame(width=500, height=400, bg="grey", colormap="new")
plot_frame.grid(row=0, column=2, rowspan=2, columnspan=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=1, pady=1)


#%% one energy window
# positions

group_1 = tk.LabelFrame(root, padx=15, pady=10, text="1-Energiefenster")
group_1.grid(row=0, column=1, padx=10, pady=5, sticky='w' + 'e')

# background group
group_1b = tk.LabelFrame(group_1, padx=15, pady=10, text="Hintergrund")
group_1b.grid(padx=10, pady=5, sticky='w' + 'e')

label_background_0d_ant = tk.Label(group_1b, text="BG 0d ant [kcts]:").grid(row=0)
label_background_0d_post = tk.Label(group_1b, text="BG 0d post [kcts]:").grid(row=0, column=3, padx=26)

entry_background_0d_ant = tk.Entry(group_1b)
entry_background_0d_ant.grid(row=0, column=1, padx=15)

entry_background_0d_post = tk.Entry(group_1b)
entry_background_0d_post.grid(row=0, column=4, padx=15)

label_background_7d_ant = tk.Label(group_1b, text="BG 7d ant [kcts]:").grid(row=1)
label_background_7d_post = tk.Label(group_1b, text="BG 7d post [kcts]:").grid(row=1, column=3, padx=26)

entry_background_7d_ant = tk.Entry(group_1b)
entry_background_7d_ant.grid(row=1, column=1, padx=15)

entry_background_7d_post = tk.Entry(group_1b)
entry_background_7d_post.grid(row=1, column=4, padx=15)

# 0 and 7 days group
group_11 = tk.LabelFrame(group_1, padx=15, pady=10, text="Counts")
group_11.grid(padx=10, pady=5, sticky='w' + 'e')

# 0 days
label_ant_counts_0d = tk.Label(group_11, text="Ant 0d [kcts]:").grid(row=0)
label_post_counts_0d = tk.Label(group_11, text="Post 0d [kcts]:").grid(row=0, column=3, padx=26)

entry_ant_counts_0d = tk.Entry(group_11)
entry_ant_counts_0d.grid(row=0, column=1, padx=10)

entry_post_counts_0d = tk.Entry(group_11)
entry_post_counts_0d.grid(row=0, column=4, padx=15)

# 7 days
label_ant_counts_7d = tk.Label(group_11, text="Ant 7d [kcts]:").grid(row=1)
label_post_counts_7d = tk.Label(group_11, text="Post 7d [kcts]:").grid(row=1, column=3, padx=26)

entry_ant_counts_7d = tk.Entry(group_11)
entry_ant_counts_7d.grid(row=1, column=1, padx=10)

entry_post_counts_7d = tk.Entry(group_11)
entry_post_counts_7d.grid(row=1, column=4, padx=15)

# retention group
group_1r = tk.LabelFrame(group_1, padx=15, pady=10, text="Retention")
group_1r.grid(padx=10, pady=5, sticky='w' + 'e')

label_retention_1 = tk.Label(group_1r, text="Tag 7 Retention [%]:").grid(row=0)
label_areaRetention_1 = tk.Label(group_1r, bg='gray', width='12', text="")
label_areaRetention_1.grid(row=0, column=1, padx=10)

# define calc button position
buttonCalculate_1 = tk.Button(group_1r, text='Berechnen!', width='10', bg='red', command=buttonCalculate_1)
buttonCalculate_1.grid(row=0, column=3, padx=160, pady=5)


#%% two energy windows
# positions

group_2 = tk.LabelFrame(root, padx=15, pady=10, text="2-Energiefenster")
group_2.grid(row=1, column=1, padx=10, pady=5, sticky='w' + 'e')

# background
group_2b = tk.LabelFrame(group_2, padx=15, pady=10, text="Hintergrund")
group_2b.grid(padx=10, pady=5, sticky='w' + 'e')

# bg energy window 1
group_2b_w1 = tk.LabelFrame(group_2b, padx=15, pady=10, text="1. Energiefenster")
group_2b_w1.grid(padx=10, pady=5, sticky='w' + 'e')

label_background_0d_ant_w1 = tk.Label(group_2b_w1, text="BG 0d ant [kcts]:").grid(row=0)
label_background_0d_post_w1 = tk.Label(group_2b_w1, text="BG 0d post [kcts]:").grid(row=0, column=3, padx=26)

entry_background_0d_ant_w1 = tk.Entry(group_2b_w1)
entry_background_0d_ant_w1.grid(row=0, column=1, padx=15)

entry_background_0d_post_w1 = tk.Entry(group_2b_w1)
entry_background_0d_post_w1.grid(row=0, column=4, padx=15)

label_background_7d_ant_w1 = tk.Label(group_2b_w1, text="BG 7d ant [kcts]:").grid(row=1)
label_background_7d_post_w1 = tk.Label(group_2b_w1, text="BG 7d post [kcts]:").grid(row=1, column=3, padx=26)

entry_background_7d_ant_w1 = tk.Entry(group_2b_w1)
entry_background_7d_ant_w1.grid(row=1, column=1, padx=15)

entry_background_7d_post_w1 = tk.Entry(group_2b_w1)
entry_background_7d_post_w1.grid(row=1, column=4, padx=15)

# bg energy window 2
group_2b_w2 = tk.LabelFrame(group_2b, padx=15, pady=10, text="2. Energiefenster")
group_2b_w2.grid(padx=10, pady=5, sticky='w' + 'e')

label_background_0d_ant_w2 = tk.Label(group_2b_w2, text="BG 0d ant [kcts]:").grid(row=0)
label_background_0d_post_w2 = tk.Label(group_2b_w2, text="BG 0d post [kcts]:").grid(row=0, column=3, padx=26)

entry_background_0d_ant_w2 = tk.Entry(group_2b_w2)
entry_background_0d_ant_w2.grid(row=0, column=1, padx=15)

entry_background_0d_post_w2 = tk.Entry(group_2b_w2)
entry_background_0d_post_w2.grid(row=0, column=4, padx=15)

label_background_7d_ant_w2 = tk.Label(group_2b_w2, text="BG 7d ant [kcts]:").grid(row=1)
label_background_7d_post_w2 = tk.Label(group_2b_w2, text="BG 7d post [kcts]:").grid(row=1, column=3, padx=26)

entry_background_7d_ant_w2 = tk.Entry(group_2b_w2)
entry_background_7d_ant_w2.grid(row=1, column=1, padx=15)

entry_background_7d_post_w2 = tk.Entry(group_2b_w2)
entry_background_7d_post_w2.grid(row=1, column=4, padx=15)

# energy window 1
group_21 = tk.LabelFrame(group_2, padx=15, pady=10, text="1. Energiefenster")
group_21.grid(padx=10, pady=5, sticky='w' + 'e')

label_ant_counts_0d_window1 = tk.Label(group_21, text="Ant 0d [kcts]:").grid(row=0)
label_post_counts_0d_window1 = tk.Label(group_21, text="Post 0d [kcts]:").grid(row=0, column=3, padx=26)

label_ant_counts_7d_window1 = tk.Label(group_21, text="Ant 7d [kcts]:").grid(row=1)
label_post_counts_7d_window1 = tk.Label(group_21, text="Post 7d [kcts]:").grid(row=1, column=3, padx=26)

entry_ant_counts_0d_window1 = tk.Entry(group_21)
entry_ant_counts_0d_window1.grid(row=0, column=1, padx=10)

entry_post_counts_0d_window1 = tk.Entry(group_21)
entry_post_counts_0d_window1.grid(row=0, column=4, padx=15)

entry_ant_counts_7d_window1 = tk.Entry(group_21)
entry_ant_counts_7d_window1.grid(row=1, column=1, padx=10)

entry_post_counts_7d_window1 = tk.Entry(group_21)
entry_post_counts_7d_window1.grid(row=1, column=4, padx=15)

# energy window 2
group_22 = tk.LabelFrame(group_2, padx=15, pady=10, text="2. Energiefenster")
group_22.grid(padx=10, pady=5, sticky='w' + 'e')

label_ant_counts_0d_window2 = tk.Label(group_22, text="Ant 0d [kcts]:").grid(row=0)
label_post_counts_0d_window2 = tk.Label(group_22, text="Post 0d [kcts]:").grid(row=0, column=3, padx=26)

label_ant_counts_7d_window2 = tk.Label(group_22, text="Ant 7d [kcts]:").grid(row=1)
label_post_counts_7d_window2 = tk.Label(group_22, text="Post 7d [kcts]:").grid(row=1, column=3, padx=26)

entry_ant_counts_0d_window2 = tk.Entry(group_22)
entry_ant_counts_0d_window2.grid(row=0, column=1, padx=10)

entry_post_counts_0d_window2 = tk.Entry(group_22)
entry_post_counts_0d_window2.grid(row=0, column=4, padx=15)

entry_ant_counts_7d_window2 = tk.Entry(group_22)
entry_ant_counts_7d_window2.grid(row=1, column=1, padx=10)

entry_post_counts_7d_window2 = tk.Entry(group_22)
entry_post_counts_7d_window2.grid(row=1, column=4, padx=15)

# retention
group_2r = tk.LabelFrame(group_2, padx=15, pady=10, text="Retention")
group_2r.grid(padx=10, pady=5, sticky='w' + 'e')

label_retention_2 = tk.Label(group_2r, text="Tag 7 Retention [%]:").grid(row=0)
label_areaRetention_2 = tk.Label(group_2r, bg='gray', width='12', text="")
label_areaRetention_2.grid(row=0, column=1, padx=10)

# define calc button position
buttonCalculate_2 = tk.Button(group_2r, text='Berechnen!', width='10', bg='red', command=buttonCalculate_2)
buttonCalculate_2.grid(row=0, column=3, padx=160, pady=5)


#%% main
root.mainloop()