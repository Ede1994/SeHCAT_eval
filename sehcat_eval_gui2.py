#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright 2021

Author: Eric Einspänner, Clinic for Radiology and Nuclear Medicine, UMMD Magdeburg (Germany)

This program is free software.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import os
import numpy as np
import math

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

### Fonts
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

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

fig2 = Figure(figsize=(4, 6), dpi=60)
ax3 = fig2.add_subplot(2,1,1)
ax4 = fig2.add_subplot(2,1,2)


#%% Functions

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

#%% Functions for GUI

# popupmsg as place holder
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

# some help instructions
def Help():
    popup = tk.Tk()
    popup.wm_title("Help")
    label = ttk.Label(popup, text=("""Alle Felder entsprechend ausfüllen. Achtung: Angaben in kilo-Counts [kcts]!
Durch das Betätigen des 'Berechnen!'-Buttons wird die Retention nach 7 Tagen in % ausgegeben!
1-Energiefenster: Diese Eingabemaske benutzen, wenn nur EIN Energiefenster für die WB genutzt wurde.
2-Energiefenster: Diese Eingabemaske benutzen, wenn nur ZWEI Energiefenster für die WB genutzt wurde.

English:
Please fill in all fields accordingly. Note: Data in kilo-counts!
Press the 'Berechnen!'-Button to get the final retention in %.
One energy window: Use this mask, if only one energy window was set for the WB.
Two energy windows: Use this mask, if two energy windows were set for the WB."""), font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

# impressum message
def Impressum():
    popup = tk.Tk()
    popup.wm_title("Impressum")
    label = ttk.Label(popup, text=("""Author: Eric Einspänner (Clinic for Radiology and Nuclear Medicine, UMMD Magdeburg (Germany))
Contact: eric.einspaenner@med.ovgu.de
GitHub: https://github.com/Ede1994/SeHCAT_eval

This program is free software."""), font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

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

#%% Spectrum Conv classes

### constructor app
class SeHCAT_eval(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self,default="tmp/nuclear.ico")
        tk.Tk.wm_title(self, "SeHCAT Eval")
        tk.Tk.geometry(self, "1600x1400")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        ### define menu
        menubar = tk.Menu(container)

        # file menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Import...", command = lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Speichern als...", command = SaveData)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command = container.quit)
        menubar.add_cascade(label="File", menu = filemenu)

        # edit menu
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Delete All", command = lambda: popupmsg("Not supported just yet!"))
        menubar.add_cascade(label="Edit", menu = editmenu)
        
        # help menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command = Help)
        helpmenu.add_command(label="Impressum", command = Impressum)
        menubar.add_cascade(label="Help", menu = helpmenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, one_energy_window, two_energy_window):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # Button: show frame
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


#%% start page/ home screen
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        label = ttk.Label(self, text="Home", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        label = ttk.Label(self, text=("""SeHCAT Eval is a open-source software tool.
        There is no promise of warranty."""), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        # patient data
        # entries
        group_patient = ttk.LabelFrame(self, text="Patientendaten")
        group_patient.pack()

        self.label_patname = tk.Label(group_patient, text="Name:").grid(row=0)
        self.entry_patname = tk.Entry(group_patient)
        self.entry_patname.grid(row=0, column=1, padx=15)

        self.label_patbirth = tk.Label(group_patient, text="Geburtsdatum:").grid(row=1)
        self.entry_patbirth = tk.Entry(group_patient)
        self.entry_patbirth.grid(row=1, column=1, padx=15)

        self.label_patheight = tk.Label(group_patient, text="Größe [cm]:").grid(row=2)
        self.entry_patheight = tk.Entry(group_patient)
        self.entry_patheight.grid(row=2, column=1, padx=15)

        self.label_patweight = tk.Label(group_patient, text="Gewicht [kg]:").grid(row=3)
        self.entry_patweight = tk.Entry(group_patient)
        self.entry_patweight.grid(row=3, column=1, padx=15)

        self.label_patactivity = tk.Label(group_patient, text="appl. Aktivität [kBq]:").grid(row=4)
        self.entry_patactivity = tk.Entry(group_patient)
        self.entry_patactivity.grid(row=4, column=1, padx=15)

        self.label_patactdate = tk.Label(group_patient, text="App.-zeitpunkt:").grid(row=5)
        self.entry_patactdate = tk.Entry(group_patient)
        self.entry_patactdate.grid(row=5, column=1, padx=15)

        self.label_pat_date_1st = tk.Label(group_patient, text="1. Messung:").grid(row=6)
        self.entry_pat_date_1st = tk.Entry(group_patient)
        self.entry_pat_date_1st.grid(row=6, column=1, padx=15)

        self.label_pat_date_2nd = tk.Label(group_patient, text="2. Messung:").grid(row=7)
        self.entry_pat_date_2nd = tk.Entry(group_patient)
        self.entry_pat_date_2nd.grid(row=7, column=1, padx=15)
        
        # buttons energy windows
        button = ttk.Button(self, text="Laden",
                            command = self.load)
        button.pack()
        
        # buttons energy windows
        button = ttk.Button(self, text="1-Energiefenster",
                            command = lambda: controller.show_frame(one_energy_window))
        button.pack()

        button2 = ttk.Button(self, text="2-Energiefenster",
                            command = lambda: controller.show_frame(two_energy_window))
        button2.pack()
    
    def load(self):
        patdata['Name'] = self.entry_patname.get()
        patdata['Birthday'] = self.entry_patbirth.get()
        patdata['Height'] = self.entry_patheight.get()
        patdata['Weight'] = self.entry_patweight.get()
        patdata['Applied Activity [kBq]'] = self.entry_patactivity.get()
        patdata['Application Date'] = self.entry_patactdate.get()
        patdata['1st Measurement'] = self.entry_pat_date_1st.get()
        patdata['2nd Measurement'] = self.entry_pat_date_2nd.get()
        popupmsg("Patientendaten erfolgreich geladen!")


#%% one energy window
class one_energy_window(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="1-Energiefenster", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        buttonHome = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        buttonHome.pack()
        
        # entries
        group_1 = ttk.LabelFrame(self, text="1-Energiefenster")
        group_1.pack()

        # background group
        group_1b = ttk.LabelFrame(group_1, text="Hintergrund")
        group_1b.pack()

        self.label_background_0d_ant = tk.Label(group_1b, text="BG 0d ant [kcts]:").grid(row=0)
        self.label_background_0d_post = tk.Label(group_1b, text="BG 0d post [kcts]:").grid(row=0, column=3, padx=26)

        self.entry_background_0d_ant = tk.Entry(group_1b)
        self.entry_background_0d_ant.grid(row=0, column=1, padx=15)

        self.entry_background_0d_post = tk.Entry(group_1b)
        self.entry_background_0d_post.grid(row=0, column=4, padx=15)

        self.label_background_7d_ant = tk.Label(group_1b, text="BG 7d ant [kcts]:").grid(row=1)
        self.label_background_7d_post = tk.Label(group_1b, text="BG 7d post [kcts]:").grid(row=1, column=3, padx=26)

        self.entry_background_7d_ant = tk.Entry(group_1b)
        self.entry_background_7d_ant.grid(row=1, column=1, padx=15)

        self.entry_background_7d_post = tk.Entry(group_1b)
        self.entry_background_7d_post.grid(row=1, column=4, padx=15)

        # 0 and 7 days group
        group_11 = ttk.LabelFrame(group_1, text="Counts")
        group_11.pack()

        # 0 days
        self.label_ant_counts_0d = tk.Label(group_11, text="Ant 0d [kcts]:").grid(row=0)
        self.label_post_counts_0d = tk.Label(group_11, text="Post 0d [kcts]:").grid(row=0, column=3, padx=26)

        self.entry_ant_counts_0d = tk.Entry(group_11)
        self.entry_ant_counts_0d.grid(row=0, column=1, padx=10)

        self.entry_post_counts_0d = tk.Entry(group_11)
        self.entry_post_counts_0d.grid(row=0, column=4, padx=15)

        # 7 days
        self.label_ant_counts_7d = tk.Label(group_11, text="Ant 7d [kcts]:").grid(row=1)
        self.label_post_counts_7d = tk.Label(group_11, text="Post 7d [kcts]:").grid(row=1, column=3, padx=26)

        self.entry_ant_counts_7d = tk.Entry(group_11)
        self.entry_ant_counts_7d.grid(row=1, column=1, padx=10)

        self.entry_post_counts_7d = tk.Entry(group_11)
        self.entry_post_counts_7d.grid(row=1, column=4, padx=15)

        # retention group
        group_1r = ttk.LabelFrame(group_1, text="Retention")
        group_1r.pack()

        self.label_retention_1 = tk.Label(group_1r, text="Tag 7 Retention [%]:").grid(row=0)
        self.label_areaRetention_1 = tk.Label(group_1r, bg='gray', width='12', text="")
        self.label_areaRetention_1.grid(row=0, column=1, padx=10)
    
        buttonCalc = ttk.Button(self, text="Berechnen", command = self.buttonCalculate_one_window)
        buttonCalc.pack()

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)
    
    ### calculation for one energy window
    def buttonCalculate_one_window(self):
        # get values
        # background ant 0d
        background_0d_ant = self.entry_background_0d_ant.get()
        if background_0d_ant == '':
            popupmsg("Fehler: Kein Hintergrund 0d ant!")
        else:
            background_0d_ant = float(background_0d_ant) * 10**3

     	# background ant 7d
        background_7d_ant = self.entry_background_7d_ant.get()
        if background_7d_ant == '':
            popupmsg("Fehler: Kein Hintergrund 7d ant!")
        else:
            background_7d_ant = float(background_7d_ant) * 10**3

     	# background post 0d
        background_0d_post = self.entry_background_0d_post.get()
        if background_0d_post == '':
            popupmsg("Fehler: Kein Hintergrund 0d post!")
        else:
            background_0d_post = float(background_0d_post) * 10**3

     	# background post 7d
        background_7d_post = self.entry_background_7d_post.get()
        if background_7d_post == '':
     	    popupmsg("Fehler: Kein Hintergrund 7d post!")
        else:
            background_7d_post = float(background_7d_post) * 10**3

     	# Ant 0d
        ant_counts_0d = self.entry_ant_counts_0d.get()
        if ant_counts_0d == '':
     	   popupmsg("Fehler: Keine ant counts 0d!")
        else:
            ant_counts_0d = float(ant_counts_0d) * 10**3

     	# Post 0d
        post_counts_0d = self.entry_post_counts_0d.get()
        if post_counts_0d == '':
            popupmsg("Fehler: Keine post counts 0d!")
        else:
            post_counts_0d = float(post_counts_0d) * 10**3

     	# Ant 7d
        ant_counts_7d = self.entry_ant_counts_7d.get()
        if ant_counts_7d == '':
            popupmsg("Fehler: Keine ant counts 7d!")
        else:
            ant_counts_7d = float(ant_counts_7d) * 10**3

     	# Post 7d
        post_counts_7d = self.entry_post_counts_7d.get()
        if post_counts_7d == '':
            popupmsg("Fehler: Keine post counts 7d!")
        else:
            post_counts_7d = float(post_counts_7d) * 10**3

        retention_1w = round(decay_factor * (np.sqrt((ant_counts_7d - background_7d_ant)*(post_counts_7d - background_7d_post)) \
                                          / np.sqrt((ant_counts_0d - background_0d_ant)*(post_counts_0d - background_0d_post))) * 100., 2)
    
        counts_0d = ((ant_counts_0d - background_0d_ant) + (post_counts_0d - background_0d_post)) / 2.
        counts_7d = ((ant_counts_7d - background_7d_ant)  + (post_counts_7d - background_7d_post)) / 2.
    
        dt_list, retention_10, retention_15 = retention_lists(counts_0d)
        dt_selen, decay_selen = selen_decay(counts_0d)

        # results; add in label areas
        self.label_areaRetention_1.config(text=str(retention_1w))
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
        ax2.annotate('Retention', xy=(dt_list[-3], retention_1w), )
        ax2.axvline(x = 0, color='red', linestyle='--', linewidth='0.33')
        ax2.axvline(x = 7, color='red', linestyle='--', linewidth='0.33')
        ax2.set_ylabel('kcts')
        ax2.set_xlabel('Tagen')
        ax2.legend()


#%% two energy windows
class two_energy_window(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="2-Energiefenster", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        buttonHome = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        buttonHome.pack()
        
        # entries
        group_2 = tk.LabelFrame(self, text="2-Energiefenster")
        group_2.pack()

        # background
        group_2b = tk.LabelFrame(group_2, text="Hintergrund")
        group_2b.pack()

        # bg energy window 1
        group_2b_w1 = tk.LabelFrame(group_2b, text="1. Energiefenster")
        group_2b_w1.pack()

        self.label_background_0d_ant_w1 = tk.Label(group_2b_w1, text="BG 0d ant [kcts]:").grid(row=0)
        self.label_background_0d_post_w1 = tk.Label(group_2b_w1, text="BG 0d post [kcts]:").grid(row=0, column=3, padx=26)

        self.entry_background_0d_ant_w1 = tk.Entry(group_2b_w1)
        self.entry_background_0d_ant_w1.grid(row=0, column=1, padx=15)

        self.entry_background_0d_post_w1 = tk.Entry(group_2b_w1)
        self.entry_background_0d_post_w1.grid(row=0, column=4, padx=15)

        self.label_background_7d_ant_w1 = tk.Label(group_2b_w1, text="BG 7d ant [kcts]:").grid(row=1)
        self.label_background_7d_post_w1 = tk.Label(group_2b_w1, text="BG 7d post [kcts]:").grid(row=1, column=3, padx=26)

        self.entry_background_7d_ant_w1 = tk.Entry(group_2b_w1)
        self.entry_background_7d_ant_w1.grid(row=1, column=1, padx=15)

        self.entry_background_7d_post_w1 = tk.Entry(group_2b_w1)
        self.entry_background_7d_post_w1.grid(row=1, column=4, padx=15)

        # bg energy window 2
        group_2b_w2 = tk.LabelFrame(group_2b, text="2. Energiefenster")
        group_2b_w2.pack()

        self.label_background_0d_ant_w2 = tk.Label(group_2b_w2, text="BG 0d ant [kcts]:").grid(row=0)
        self.label_background_0d_post_w2 = tk.Label(group_2b_w2, text="BG 0d post [kcts]:").grid(row=0, column=3, padx=26)

        self.entry_background_0d_ant_w2 = tk.Entry(group_2b_w2)
        self.entry_background_0d_ant_w2.grid(row=0, column=1, padx=15)

        self.entry_background_0d_post_w2 = tk.Entry(group_2b_w2)
        self.entry_background_0d_post_w2.grid(row=0, column=4, padx=15)

        self.label_background_7d_ant_w2 = tk.Label(group_2b_w2, text="BG 7d ant [kcts]:").grid(row=1)
        self.label_background_7d_post_w2 = tk.Label(group_2b_w2, text="BG 7d post [kcts]:").grid(row=1, column=3, padx=26)

        self.entry_background_7d_ant_w2 = tk.Entry(group_2b_w2)
        self.entry_background_7d_ant_w2.grid(row=1, column=1, padx=15)

        self.entry_background_7d_post_w2 = tk.Entry(group_2b_w2)
        self.entry_background_7d_post_w2.grid(row=1, column=4, padx=15)

        # energy window 1
        group_21 = tk.LabelFrame(group_2, text="1. Energiefenster")
        group_21.pack()

        self.label_ant_counts_0d_window1 = tk.Label(group_21, text="Ant 0d [kcts]:").grid(row=0)
        self.label_post_counts_0d_window1 = tk.Label(group_21, text="Post 0d [kcts]:").grid(row=0, column=3, padx=26)

        self.label_ant_counts_7d_window1 = tk.Label(group_21, text="Ant 7d [kcts]:").grid(row=1)
        self.label_post_counts_7d_window1 = tk.Label(group_21, text="Post 7d [kcts]:").grid(row=1, column=3, padx=26)

        self.entry_ant_counts_0d_window1 = tk.Entry(group_21)
        self.entry_ant_counts_0d_window1.grid(row=0, column=1, padx=10)

        self.entry_post_counts_0d_window1 = tk.Entry(group_21)
        self.entry_post_counts_0d_window1.grid(row=0, column=4, padx=15)

        self.entry_ant_counts_7d_window1 = tk.Entry(group_21)
        self.entry_ant_counts_7d_window1.grid(row=1, column=1, padx=10)

        self.entry_post_counts_7d_window1 = tk.Entry(group_21)
        self.entry_post_counts_7d_window1.grid(row=1, column=4, padx=15)

        # energy window 2
        group_22 = tk.LabelFrame(group_2, text="2. Energiefenster")
        group_22.pack()

        self.label_ant_counts_0d_window2 = tk.Label(group_22, text="Ant 0d [kcts]:").grid(row=0)
        self.label_post_counts_0d_window2 = tk.Label(group_22, text="Post 0d [kcts]:").grid(row=0, column=3, padx=26)

        self.label_ant_counts_7d_window2 = tk.Label(group_22, text="Ant 7d [kcts]:").grid(row=1)
        self.label_post_counts_7d_window2 = tk.Label(group_22, text="Post 7d [kcts]:").grid(row=1, column=3, padx=26)

        self.entry_ant_counts_0d_window2 = tk.Entry(group_22)
        self.entry_ant_counts_0d_window2.grid(row=0, column=1, padx=10)

        self.entry_post_counts_0d_window2 = tk.Entry(group_22)
        self.entry_post_counts_0d_window2.grid(row=0, column=4, padx=15)

        self.entry_ant_counts_7d_window2 = tk.Entry(group_22)
        self.entry_ant_counts_7d_window2.grid(row=1, column=1, padx=10)

        self.entry_post_counts_7d_window2 = tk.Entry(group_22)
        self.entry_post_counts_7d_window2.grid(row=1, column=4, padx=15)

        # retention
        group_2r = tk.LabelFrame(group_2, text="Retention")
        group_2r.pack()

        self.label_retention_2 = tk.Label(group_2r, text="Tag 7 Retention [%]:").grid(row=0)
        self.label_areaRetention_2 = tk.Label(group_2r, bg='gray', width='12', text="")
        self.label_areaRetention_2.grid(row=0, column=1, padx=10)
    
        buttonCalc = ttk.Button(self, text="Berechnen", command = self.buttonCalculate_two_windows)
        buttonCalc.pack()

        canvas2 = FigureCanvasTkAgg(fig2, self)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar2 = NavigationToolbar2Tk(canvas2, self)
        toolbar2.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    ### calculation for two energy windows
    def buttonCalculate_two_windows(self):
        # get values
        #background ant 0d w2
        background_0d_ant_w1 = self.entry_background_0d_ant_w1.get()
        if background_0d_ant_w1 == '':
            popupmsg("Fehler: Kein Hintergrund 0d ant 1-Fenster!")
        else:
            background_0d_ant_w1 = float(background_0d_ant_w1) * 10**3

     	# background 0d post w2
        background_0d_post_w1 = self.entry_background_0d_post_w1.get()
        if background_0d_post_w1 == '':
            popupmsg("Fehler: Kein Hintergrund 0d post 1-Fenster!")
        else:
            background_0d_post_w1 = float(background_0d_post_w1) * 10**3

        # background ant 7d w2
        background_7d_ant_w1 = self.entry_background_7d_ant_w1.get()
        if background_7d_ant_w1 == '':
            popupmsg("Fehler: Kein Hintergrund 7d ant 1-Fenster!")
        else:
            background_7d_ant_w1 = float(background_7d_ant_w1) * 10**3

     	# background post 7d w2
        background_7d_post_w1 = self.entry_background_7d_post_w1.get()
        if background_7d_post_w1 == '':
            popupmsg("Fehler: Kein Hintergrund 7d post 1-Fenster!")
        else:
            background_7d_post_w1 = float(background_7d_post_w1) * 10**3

        # backgound ant 0d w2
        background_0d_ant_w2 = self.entry_background_0d_ant_w2.get()
        if background_0d_ant_w2 == '':
            popupmsg("Fehler: Kein Hintergrund 0d ant 2-Fenster!")
        else:
            background_0d_ant_w2 = float(background_0d_ant_w2) * 10**3

     	# background 0d post w2
        background_0d_post_w2 = self.entry_background_0d_post_w2.get()
        if background_0d_post_w2 == '':
            popupmsg("Fehler: Kein Hintergrund 0d post 2-Fenster!")
        else:
            background_0d_post_w2 = float(background_0d_post_w2) * 10**3

        # background ant 7d w2
        background_7d_ant_w2 = self.entry_background_7d_ant_w2.get()
        if background_7d_ant_w2 == '':
            popupmsg("Fehler: Kein Hintergrund 7d ant 2-Fenster!")
        else:
            background_7d_ant_w2 = float(background_7d_ant_w2) * 10**3

     	# background post 7d w2
        background_7d_post_w2 = self.entry_background_7d_post_w2.get()
        if background_7d_post_w2 == '':
            popupmsg("Fehler: Kein Hintergrund 7d post 2-Fenster!")
        else:
            background_7d_post_w2 = float(background_7d_post_w2) * 10**3

        # window 1
        # ant 0d
        ant_counts_0d_window1 = self.entry_ant_counts_0d_window1.get()
        if ant_counts_0d_window1 == '':
            popupmsg("Fehler: Keine ant counts 0d für 1-Energiefenster!")
        else:
            ant_counts_0d_window1 = float(ant_counts_0d_window1) * 10**3

     	# Post 0d
        post_counts_0d_window1 = self.entry_post_counts_0d_window1.get()
        if post_counts_0d_window1 == '':
            popupmsg("Fehler: Keine post counts 0d für 1-Energiefenster!")
        else:
            post_counts_0d_window1 = float(post_counts_0d_window1) * 10**3

     	# Ant 7d
        ant_counts_7d_window1 = self.entry_ant_counts_7d_window1.get()
        if ant_counts_7d_window1 == '':
            popupmsg("Fehler: Keine ant counts 7d für 1-Energiefenster!")
        else:
            ant_counts_7d_window1 = float(ant_counts_7d_window1) * 10**3

     	# Post 7d
        post_counts_7d_window1 = self.entry_post_counts_7d_window1.get()
        if post_counts_7d_window1 == '':
            popupmsg("Fehler: Keine post counts 7d für 1-Energiefenster!")
        else:
            post_counts_7d_window1 = float(post_counts_7d_window1) * 10**3

        # window 2
        # Ant 0d
        ant_counts_0d_window2 = self.entry_ant_counts_0d_window2.get()
        if ant_counts_0d_window2 == '':
            popupmsg("Fehler: Keine ant counts 0d für 2-Energiefenster!")
        else:
            ant_counts_0d_window2 = float(ant_counts_0d_window2) * 10**3

     	# Post 0d
        post_counts_0d_window2 = self.entry_post_counts_0d_window2.get()
        if post_counts_0d_window2 == '':
            popupmsg("Fehler: Keine post counts 0d für 2-Energiefenster!")
        else:
            post_counts_0d_window2 = float(post_counts_0d_window2) * 10**3

     	# Ant 7d
        ant_counts_7d_window2 = self.entry_ant_counts_7d_window2.get()
        if ant_counts_7d_window2 == '':
             popupmsg("Fehler: Keine ant counts d für 2-Energiefenster!")
        else:
            ant_counts_7d_window2 = float(ant_counts_7d_window2) * 10**3

     	# Post 7d
        post_counts_7d_window2 = self.entry_post_counts_7d_window2.get()
        if post_counts_7d_window2 == '':
            popupmsg("Fehler: Keine post counts 7d für 2-Energiefenster!")
        else:
            post_counts_7d_window2 = float(post_counts_7d_window2) * 10**3

        # retention = (window1 + window2)/2 (round -> .00)
        retention_2w = round(decay_factor * (np.sqrt((ant_counts_7d_window1 + ant_counts_7d_window2 - background_7d_ant_w1 - background_7d_ant_w2)*(post_counts_7d_window1 + post_counts_7d_window2 - background_7d_post_w1 - background_7d_post_w2))) \
                      / np.sqrt((ant_counts_0d_window1 + ant_counts_0d_window2 - background_0d_ant_w1 - background_0d_ant_w2)*(post_counts_0d_window1 + post_counts_0d_window2 - background_0d_post_w1 - background_0d_post_w2)) * 100., 2)

        counts_0d = ((ant_counts_0d_window1 + ant_counts_0d_window2 - background_0d_ant_w1 - background_0d_ant_w2) + (post_counts_0d_window1 + post_counts_0d_window2 - background_0d_post_w1 - background_0d_post_w2)) / 2.
        counts_7d = ((ant_counts_7d_window1 + ant_counts_7d_window2 - background_7d_ant_w1 - background_7d_ant_w2) + (post_counts_7d_window1 + post_counts_7d_window2 - background_7d_post_w1 - background_7d_post_w2)) / 2.
        
        # results; add in label areas
        self.label_areaRetention_2.config(text=str(retention_2w))
        patdata['Retention 2-Fenster [%]'] = retention_2w
    
        dt_list, retention_10, retention_15 = retention_lists(counts_0d)
        dt_selen, decay_selen = selen_decay(counts_0d)

        # plot
        ax3.clear()
        ax4.clear()
    
        #ax3.set_title('kcts vs Tagen')
        ax3.plot(0, counts_0d, 'o', label='kcts 0d')
        ax3.plot(7, counts_7d, 'o', label='kcts 7d')
        ax3.plot(dt_selen, decay_selen, label='physikalischer Zerfall Se-75')
        ax3.axvline(x = 0, color='red', linestyle='--', linewidth='0.33')
        ax3.axvline(x = 7, color='red', linestyle='--', linewidth='0.33')
        ax3.set_ylabel('kcts')
        ax3.set_xlabel('Tagen')
        ax3.legend()
    
        ax4.plot(dt_list, retention_10, label='Retention = 10%')
        ax4.plot(dt_list, retention_15, label='Retention = 15%')
        ax4.plot(7., counts_7d, 'o')
        ax4.annotate('Retention', xy=(dt_list[-3], retention_2w), )
        ax4.axvline(x = 0, color='red', linestyle='--', linewidth='0.33')
        ax4.axvline(x = 7, color='red', linestyle='--', linewidth='0.33')
        ax4.set_ylabel('kcts')
        ax4.set_xlabel('Tagen')
        ax4.legend()


#%% start application

app = SeHCAT_eval()
app.mainloop()