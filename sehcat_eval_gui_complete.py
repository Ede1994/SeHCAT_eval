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

from functions import selen_decay, retention_lists, retention_1w_calc, retention_2w_calc
from gui_functions import popupmsg, Help, Impressum, dcm2header, dcm2data, SaveData

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
fig = Figure(figsize=(6, 2), dpi=100)
ax = fig.add_subplot(1,1,1)


#%% Spectrum Conv classes

### constructor app
class SeHCAT_eval(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self,default="tmp/nuclear.ico")
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
        filemenu.add_command(label="Speichern als...", command = lambda: SaveData(fig, patdata))
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
        
        ### patient data
        ### entries
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

        # button load dicom header
        button = ttk.Button(self, text="Patientendaten laden",
                            command = self.buttonImport_Header)
        button.pack()
        
        # button save patdata
        button = ttk.Button(self, text="Patientendaten speichern",
                            command = self.load)
        button.pack()
        
        # buttons energy windows
        button = ttk.Button(self, text="1-Energiefenster: 137 keV",
                            command = lambda: controller.show_frame(one_energy_window))
        button.pack()

        button2 = ttk.Button(self, text="2-Energiefenster: 137 und 280 keV",
                            command = lambda: controller.show_frame(two_energy_window))
        button2.pack()

    ### Load Buttons
    def buttonImport_Header(self):
        # open dialog
        file = filedialog.askopenfile(title="Load data...", mode='r', filetypes=[("All files", "*.*")])

        # extract filename as str
        filename = str(file.name)

        dcm2header(filename, patdata)
        
        self.entry_patname.insert(0, patdata['Name'])
        self.entry_patbirth.insert(0, patdata['Birthday'])
        self.entry_patheight.insert(0, patdata['Height'])
        self.entry_patweight.insert(0, patdata['Weight'])

    
    # store patient infos in dic
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
        label = ttk.Label(self, text="1-Energiefenster: 137 keV", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        buttonHome = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        buttonHome.pack()
        
        ### entries
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

        button_loadBG_0day = ttk.Button(group_1b, text="Load BG Tag 0",
                            command = self.buttonImport_BG_0d)
        button_loadBG_0day.grid(row=0, column=5, padx=15)

        self.label_background_7d_ant = tk.Label(group_1b, text="BG 7d ant [kcts]:").grid(row=1)
        self.label_background_7d_post = tk.Label(group_1b, text="BG 7d post [kcts]:").grid(row=1, column=3, padx=26)

        self.entry_background_7d_ant = tk.Entry(group_1b)
        self.entry_background_7d_ant.grid(row=1, column=1, padx=15)

        self.entry_background_7d_post = tk.Entry(group_1b)
        self.entry_background_7d_post.grid(row=1, column=4, padx=15)

        button_loadBG_7day = ttk.Button(group_1b, text="Load BG Tag 7",
                            command = self.buttonImport_BG_7d)
        button_loadBG_7day.grid(row=1, column=5, padx=15)

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

        button_loadWB_0day = ttk.Button(group_11, text="Load WB Tag 0",
                            command = self.buttonImport_WB_0d)
        button_loadWB_0day.grid(row=0, column=5, padx=15)

        # 7 days
        self.label_ant_counts_7d = tk.Label(group_11, text="Ant 7d [kcts]:").grid(row=1)
        self.label_post_counts_7d = tk.Label(group_11, text="Post 7d [kcts]:").grid(row=1, column=3, padx=26)

        self.entry_ant_counts_7d = tk.Entry(group_11)
        self.entry_ant_counts_7d.grid(row=1, column=1, padx=10)

        self.entry_post_counts_7d = tk.Entry(group_11)
        self.entry_post_counts_7d.grid(row=1, column=4, padx=15)

        button_loadWB_7day = ttk.Button(group_11, text="Load WB Tag 7",
                            command = self.buttonImport_WB_7d)
        button_loadWB_7day.grid(row=1, column=5, padx=15)

        # retention group
        group_1r = ttk.LabelFrame(group_1, text="Retention")
        group_1r.pack()

        self.label_retention_1 = tk.Label(group_1r, text="Tag 7 Retention [%]:").grid(row=0)
        self.label_areaRetention_1 = tk.Label(group_1r, bg='gray', width='12', text="")
        self.label_areaRetention_1.grid(row=0, column=1, padx=10)

        # Button: calculation
        buttonCalc = ttk.Button(self, text="Berechnen", command = self.buttonCalculate_one_window)
        buttonCalc.pack()

        ### plot area
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

    ### Load Buttons
    def buttonImport_BG_0d(self):
        # open dialog
        file = filedialog.askopenfile(title="Load data...", mode='r', filetypes=[("All files", "*.*")])

        # extract filename as str
        filename = str(file.name)

        ant, post = dcm2data(filename)
        
        self.entry_background_0d_ant.insert(10, ant)
        self.entry_background_0d_post.insert(10, post)

    def buttonImport_BG_7d(self):
        # open dialog
        file = filedialog.askopenfile(title="Load data...", mode='r', filetypes=[("All files", "*.*")])

        # extract filename as str
        filename = str(file.name)

        ant, post = dcm2data(filename)
        
        self.entry_background_7d_ant.insert(10, ant)
        self.entry_background_7d_post.insert(10, post)

    def buttonImport_WB_0d(self):
        # open dialog
        file = filedialog.askopenfile(title="Load data...", mode='r', filetypes=[("All files", "*.*")])

        # extract filename as str
        filename = str(file.name)

        ant, post = dcm2data(filename)
        
        self.entry_ant_counts_0d.insert(10, ant)
        self.entry_post_counts_0d.insert(10, post)

    def buttonImport_WB_7d(self):
        # open dialog
        file = filedialog.askopenfile(title="Load data...", mode='r', filetypes=[("All files", "*.*")])

        # extract filename as str
        filename = str(file.name)

        ant, post = dcm2data(filename)
        
        self.entry_ant_counts_7d.insert(10, ant)
        self.entry_post_counts_7d.insert(10, post)
    
    ### calculation for one energy window
    def buttonCalculate_one_window(self):
        ### get values
        # background ant 0d
        background_0d_ant = self.entry_background_0d_ant.get()
        if background_0d_ant == '':
            popupmsg("Fehler: Kein Hintergrund 0d ant!")
        else:
            background_0d_ant = float(background_0d_ant)

     	# background ant 7d
        background_7d_ant = self.entry_background_7d_ant.get()
        if background_7d_ant == '':
            popupmsg("Fehler: Kein Hintergrund 7d ant!")
        else:
            background_7d_ant = float(background_7d_ant)

     	# background post 0d
        background_0d_post = self.entry_background_0d_post.get()
        if background_0d_post == '':
            popupmsg("Fehler: Kein Hintergrund 0d post!")
        else:
            background_0d_post = float(background_0d_post)

     	# background post 7d
        background_7d_post = self.entry_background_7d_post.get()
        if background_7d_post == '':
     	    popupmsg("Fehler: Kein Hintergrund 7d post!")
        else:
            background_7d_post = float(background_7d_post)

     	# Ant 0d
        ant_counts_0d = self.entry_ant_counts_0d.get()
        if ant_counts_0d == '':
     	   popupmsg("Fehler: Keine ant counts 0d!")
        else:
            ant_counts_0d = float(ant_counts_0d)

     	# Post 0d
        post_counts_0d = self.entry_post_counts_0d.get()
        if post_counts_0d == '':
            popupmsg("Fehler: Keine post counts 0d!")
        else:
            post_counts_0d = float(post_counts_0d)

     	# Ant 7d
        ant_counts_7d = self.entry_ant_counts_7d.get()
        if ant_counts_7d == '':
            popupmsg("Fehler: Keine ant counts 7d!")
        else:
            ant_counts_7d = float(ant_counts_7d)

     	# Post 7d
        post_counts_7d = self.entry_post_counts_7d.get()
        if post_counts_7d == '':
            popupmsg("Fehler: Keine post counts 7d!")
        else:
            post_counts_7d = float(post_counts_7d)

        ### retention
        retention_1w = retention_1w_calc(decay_factor, ant_counts_0d, ant_counts_7d, background_0d_ant, background_7d_ant, post_counts_0d, post_counts_7d, background_0d_post, background_7d_post)
    
        counts_0d = ((ant_counts_0d - background_0d_ant) + (post_counts_0d - background_0d_post)) / 2.
        counts_7d = ((ant_counts_7d - background_7d_ant)  + (post_counts_7d - background_7d_post)) / 2.
    
        dt_list, retention_10, retention_15 = retention_lists(counts_0d, T_75se)
        dt_selen, decay_selen = selen_decay(counts_0d, T_75se)

        ### results; add in label areas
        self.label_areaRetention_1.config(text=str(retention_1w))
        patdata['Retention 1-Fenster [%]'] = retention_1w
        
        ### plot
        ax.clear()
    
        ax.plot(dt_list, retention_10, label='Retention = 10%')
        ax.plot(dt_list, retention_15, label='Retention = 15%')
        ax.plot(7., counts_7d, 'o')
        ax.annotate('Retention', xy=(7.1, counts_7d))
        ax.axvline(x = 0, color='red', linestyle='--', linewidth='0.33')
        ax.axvline(x = 7, color='red', linestyle='--', linewidth='0.33')
        ax.set_ylabel('kcts')
        ax.set_xlabel('Tagen')
        ax.legend()


#%% two energy windows

class two_energy_window(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="2-Energiefenster", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        buttonHome = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        buttonHome.pack()
        
        ### entries
        group_2 = tk.LabelFrame(self, text="2-Energiefenster: 137 und 280 keV")
        group_2.pack()

        # background
        group_2b = tk.LabelFrame(group_2, text="Hintergrund")
        group_2b.pack()

        # bg day 0
        group_2b_w1 = tk.LabelFrame(group_2b, text="BG Tag 0")
        group_2b_w1.pack()

        self.label_background_0d_ant_w1 = tk.Label(group_2b_w1, text="Fenster 1 - BG 0d ant [kcts]:").grid(row=0)
        self.label_background_0d_post_w1 = tk.Label(group_2b_w1, text="BG 0d post [kcts]:").grid(row=0, column=3, padx=26)

        self.entry_background_0d_ant_w1 = tk.Entry(group_2b_w1)
        self.entry_background_0d_ant_w1.grid(row=0, column=1, padx=15)

        self.entry_background_0d_post_w1 = tk.Entry(group_2b_w1)
        self.entry_background_0d_post_w1.grid(row=0, column=4, padx=15)
        
        self.label_background_0d_ant_w2 = tk.Label(group_2b_w1, text="Fenster 2 - BG 0d ant [kcts]:").grid(row=1)
        self.label_background_0d_post_w2 = tk.Label(group_2b_w1, text="BG 0d post [kcts]:").grid(row=1, column=3, padx=26)

        self.entry_background_0d_ant_w2 = tk.Entry(group_2b_w1)
        self.entry_background_0d_ant_w2.grid(row=1, column=1, padx=15)

        self.entry_background_0d_post_w2 = tk.Entry(group_2b_w1)
        self.entry_background_0d_post_w2.grid(row=1, column=4, padx=15)

        button_loadBG_0day = ttk.Button(group_2b_w1, text="Load BG Tag 0",
                            command = self.buttonImport_BG_0d)
        button_loadBG_0day.grid(row=1, column=5, padx=15)

        # bg day 7
        group_2b_w2 = tk.LabelFrame(group_2b, text="BG Tag 7")
        group_2b_w2.pack()

        self.label_background_7d_ant_w1 = tk.Label(group_2b_w2, text="Fenster 1 - BG 7d ant [kcts]:").grid(row=0)
        self.label_background_7d_post_w1 = tk.Label(group_2b_w2, text="BG 7d post [kcts]:").grid(row=0, column=3, padx=26)

        self.entry_background_7d_ant_w1 = tk.Entry(group_2b_w2)
        self.entry_background_7d_ant_w1.grid(row=0, column=1, padx=15)

        self.entry_background_7d_post_w1 = tk.Entry(group_2b_w2)
        self.entry_background_7d_post_w1.grid(row=0, column=4, padx=15)

        self.label_background_7d_ant_w2 = tk.Label(group_2b_w2, text="Fenster 2 - BG 7d ant [kcts]:").grid(row=1)
        self.label_background_7d_post_w2 = tk.Label(group_2b_w2, text="BG 7d post [kcts]:").grid(row=1, column=3, padx=26)

        self.entry_background_7d_ant_w2 = tk.Entry(group_2b_w2)
        self.entry_background_7d_ant_w2.grid(row=1, column=1, padx=15)

        self.entry_background_7d_post_w2 = tk.Entry(group_2b_w2)
        self.entry_background_7d_post_w2.grid(row=1, column=4, padx=15)

        button_loadBG_7day = ttk.Button(group_2b_w2, text="Load BG Tag 7",
                            command = self.buttonImport_BG_7d)
        button_loadBG_7day.grid(row=1, column=5, padx=15)

        # WB day 0
        group_21 = tk.LabelFrame(group_2, text="WB Tag 0")
        group_21.pack()

        self.label_ant_counts_0d_window1 = tk.Label(group_21, text="Fenster 1 - Ant 0d [kcts]:").grid(row=0)
        self.label_post_counts_0d_window1 = tk.Label(group_21, text="Post 0d [kcts]:").grid(row=0, column=3, padx=26)

        self.entry_ant_counts_0d_window1 = tk.Entry(group_21)
        self.entry_ant_counts_0d_window1.grid(row=0, column=1, padx=10)

        self.entry_post_counts_0d_window1 = tk.Entry(group_21)
        self.entry_post_counts_0d_window1.grid(row=0, column=4, padx=15)
        
        self.label_ant_counts_0d_window2 = tk.Label(group_21, text="Fenster 2 - Ant 0d [kcts]:").grid(row=1)
        self.label_post_counts_0d_window2 = tk.Label(group_21, text="Post 0d [kcts]:").grid(row=1, column=3, padx=26)

        self.entry_ant_counts_0d_window2 = tk.Entry(group_21)
        self.entry_ant_counts_0d_window2.grid(row=1, column=1, padx=10)

        self.entry_post_counts_0d_window2 = tk.Entry(group_21)
        self.entry_post_counts_0d_window2.grid(row=1, column=4, padx=15)
        
        button_loadWB_0day = ttk.Button(group_21, text="Load WB Tag 0",
                            command = self.buttonImport_WB_0d)
        button_loadWB_0day.grid(row=1, column=5, padx=15)

        # WB day 7
        group_22 = tk.LabelFrame(group_2, text="WB Tag 7")
        group_22.pack()

        self.label_ant_counts_7d_window1 = tk.Label(group_22, text="Fenster 1 - Ant 7d [kcts]:").grid(row=0)
        self.label_post_counts_7d_window1 = tk.Label(group_22, text="Post 7d [kcts]:").grid(row=0, column=3, padx=26)

        self.entry_ant_counts_7d_window1 = tk.Entry(group_22)
        self.entry_ant_counts_7d_window1.grid(row=0, column=1, padx=10)

        self.entry_post_counts_7d_window1 = tk.Entry(group_22)
        self.entry_post_counts_7d_window1.grid(row=0, column=4, padx=15)

        self.label_ant_counts_7d_window2 = tk.Label(group_22, text="Fenster 2 - Ant 7d [kcts]:").grid(row=1)
        self.label_post_counts_7d_window2 = tk.Label(group_22, text="Post 7d [kcts]:").grid(row=1, column=3, padx=26)

        self.entry_ant_counts_7d_window2 = tk.Entry(group_22)
        self.entry_ant_counts_7d_window2.grid(row=1, column=1, padx=10)

        self.entry_post_counts_7d_window2 = tk.Entry(group_22)
        self.entry_post_counts_7d_window2.grid(row=1, column=4, padx=15)
        
        button_loadWB_7day = ttk.Button(group_22, text="Load WB Tag 7",
                            command = self.buttonImport_WB_7d)
        button_loadWB_7day.grid(row=1, column=5, padx=15)

        # retention
        group_2r = tk.LabelFrame(group_2, text="Retention")
        group_2r.pack()

        self.label_retention_2 = tk.Label(group_2r, text="Tag 7 Retention [%]:").grid(row=0)
        self.label_areaRetention_2 = tk.Label(group_2r, bg='gray', width='12', text="")
        self.label_areaRetention_2.grid(row=0, column=1, padx=10)
    
        buttonCalc = ttk.Button(self, text="Berechnen", command = self.buttonCalculate_two_windows)
        buttonCalc.pack()

        canvas2 = FigureCanvasTkAgg(fig, self)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar2 = NavigationToolbar2Tk(canvas2, self)
        toolbar2.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def buttonImport_BG_0d(self):
        # open dialog
        file = filedialog.askopenfile(title="Load data...", mode='r', filetypes=[("All files", "*.*")])

        # extract filename as str
        filename = str(file.name)

        ant_w1, post_w1, ant_w2, post_w2 = dcm2data(filename)
        
        self.entry_background_0d_ant_w1.insert(10, ant_w1)
        self.entry_background_0d_post_w1.insert(10, post_w1)
        self.entry_background_0d_ant_w2.insert(10, ant_w2)
        self.entry_background_0d_post_w2.insert(10, post_w2)

    def buttonImport_BG_7d(self):
        # open dialog
        file = filedialog.askopenfile(title="Load data...", mode='r', filetypes=[("All files", "*.*")])

        # extract filename as str
        filename = str(file.name)

        ant_w1, post_w1, ant_w2, post_w2 = dcm2data(filename)
        
        self.entry_background_7d_ant_w1.insert(10, ant_w1)
        self.entry_background_7d_post_w1.insert(10, post_w1)
        self.entry_background_7d_ant_w2.insert(10, ant_w2)
        self.entry_background_7d_post_w2.insert(10, post_w2)

    def buttonImport_WB_0d(self):
        # open dialog
        file = filedialog.askopenfile(title="Load data...", mode='r', filetypes=[("All files", "*.*")])

        # extract filename as str
        filename = str(file.name)

        ant_w1, post_w1, ant_w2, post_w2 = dcm2data(filename)
        
        self.entry_ant_counts_0d_window1.insert(10, ant_w1)
        self.entry_post_counts_0d_window1.insert(10, post_w1)
        self.entry_ant_counts_0d_window2.insert(10, ant_w2)
        self.entry_post_counts_0d_window2.insert(10, post_w2)

    def buttonImport_WB_7d(self):
        # open dialog
        file = filedialog.askopenfile(title="Load data...", mode='r', filetypes=[("All files", "*.*")])

        # extract filename as str
        filename = str(file.name)

        ant_w1, post_w1, ant_w2, post_w2 = dcm2data(filename)
        
        self.entry_ant_counts_7d_window1.insert(10, ant_w1)
        self.entry_post_counts_7d_window1.insert(10, post_w1)
        self.entry_ant_counts_7d_window2.insert(10, ant_w2)
        self.entry_post_counts_7d_window2.insert(10, post_w2)

    ### calculation for two energy windows
    def buttonCalculate_two_windows(self):
        ### get values
        #background ant 0d w2
        background_0d_ant_w1 = self.entry_background_0d_ant_w1.get()
        if background_0d_ant_w1 == '':
            popupmsg("Fehler: Kein Hintergrund 0d ant 1-Fenster!")
        else:
            background_0d_ant_w1 = float(background_0d_ant_w1)

     	# background 0d post w2
        background_0d_post_w1 = self.entry_background_0d_post_w1.get()
        if background_0d_post_w1 == '':
            popupmsg("Fehler: Kein Hintergrund 0d post 1-Fenster!")
        else:
            background_0d_post_w1 = float(background_0d_post_w1)

        # background ant 7d w2
        background_7d_ant_w1 = self.entry_background_7d_ant_w1.get()
        if background_7d_ant_w1 == '':
            popupmsg("Fehler: Kein Hintergrund 7d ant 1-Fenster!")
        else:
            background_7d_ant_w1 = float(background_7d_ant_w1)

     	# background post 7d w2
        background_7d_post_w1 = self.entry_background_7d_post_w1.get()
        if background_7d_post_w1 == '':
            popupmsg("Fehler: Kein Hintergrund 7d post 1-Fenster!")
        else:
            background_7d_post_w1 = float(background_7d_post_w1)

        # backgound ant 0d w2
        background_0d_ant_w2 = self.entry_background_0d_ant_w2.get()
        if background_0d_ant_w2 == '':
            popupmsg("Fehler: Kein Hintergrund 0d ant 2-Fenster!")
        else:
            background_0d_ant_w2 = float(background_0d_ant_w2)

     	# background 0d post w2
        background_0d_post_w2 = self.entry_background_0d_post_w2.get()
        if background_0d_post_w2 == '':
            popupmsg("Fehler: Kein Hintergrund 0d post 2-Fenster!")
        else:
            background_0d_post_w2 = float(background_0d_post_w2)

        # background ant 7d w2
        background_7d_ant_w2 = self.entry_background_7d_ant_w2.get()
        if background_7d_ant_w2 == '':
            popupmsg("Fehler: Kein Hintergrund 7d ant 2-Fenster!")
        else:
            background_7d_ant_w2 = float(background_7d_ant_w2)

     	# background post 7d w2
        background_7d_post_w2 = self.entry_background_7d_post_w2.get()
        if background_7d_post_w2 == '':
            popupmsg("Fehler: Kein Hintergrund 7d post 2-Fenster!")
        else:
            background_7d_post_w2 = float(background_7d_post_w2)

        # window 1
        # ant 0d
        ant_counts_0d_window1 = self.entry_ant_counts_0d_window1.get()
        if ant_counts_0d_window1 == '':
            popupmsg("Fehler: Keine ant counts 0d für 1-Energiefenster!")
        else:
            ant_counts_0d_window1 = float(ant_counts_0d_window1)

     	# Post 0d
        post_counts_0d_window1 = self.entry_post_counts_0d_window1.get()
        if post_counts_0d_window1 == '':
            popupmsg("Fehler: Keine post counts 0d für 1-Energiefenster!")
        else:
            post_counts_0d_window1 = float(post_counts_0d_window1)

     	# Ant 7d
        ant_counts_7d_window1 = self.entry_ant_counts_7d_window1.get()
        if ant_counts_7d_window1 == '':
            popupmsg("Fehler: Keine ant counts 7d für 1-Energiefenster!")
        else:
            ant_counts_7d_window1 = float(ant_counts_7d_window1)

     	# Post 7d
        post_counts_7d_window1 = self.entry_post_counts_7d_window1.get()
        if post_counts_7d_window1 == '':
            popupmsg("Fehler: Keine post counts 7d für 1-Energiefenster!")
        else:
            post_counts_7d_window1 = float(post_counts_7d_window1)

        # window 2
        # Ant 0d
        ant_counts_0d_window2 = self.entry_ant_counts_0d_window2.get()
        if ant_counts_0d_window2 == '':
            popupmsg("Fehler: Keine ant counts 0d für 2-Energiefenster!")
        else:
            ant_counts_0d_window2 = float(ant_counts_0d_window2)

     	# Post 0d
        post_counts_0d_window2 = self.entry_post_counts_0d_window2.get()
        if post_counts_0d_window2 == '':
            popupmsg("Fehler: Keine post counts 0d für 2-Energiefenster!")
        else:
            post_counts_0d_window2 = float(post_counts_0d_window2)

     	# Ant 7d
        ant_counts_7d_window2 = self.entry_ant_counts_7d_window2.get()
        if ant_counts_7d_window2 == '':
             popupmsg("Fehler: Keine ant counts d für 2-Energiefenster!")
        else:
            ant_counts_7d_window2 = float(ant_counts_7d_window2)

     	# Post 7d
        post_counts_7d_window2 = self.entry_post_counts_7d_window2.get()
        if post_counts_7d_window2 == '':
            popupmsg("Fehler: Keine post counts 7d für 2-Energiefenster!")
        else:
            post_counts_7d_window2 = float(post_counts_7d_window2)

        ### retention = (window1 + window2)/2 (round -> .00)
        retention_2w = retention_2w_calc(decay_factor, ant_counts_0d_window1, ant_counts_0d_window2, ant_counts_7d_window1, ant_counts_7d_window2, background_0d_ant_w1, background_0d_ant_w2, background_7d_ant_w1, background_7d_ant_w2, post_counts_0d_window1, post_counts_0d_window2, post_counts_7d_window1, post_counts_7d_window2, background_0d_post_w1, background_0d_post_w2, background_7d_post_w1, background_7d_post_w2)

        counts_0d = ((ant_counts_0d_window1 + ant_counts_0d_window2 - background_0d_ant_w1 - background_0d_ant_w2) + (post_counts_0d_window1 + post_counts_0d_window2 - background_0d_post_w1 - background_0d_post_w2)) / 2.
        counts_7d = ((ant_counts_7d_window1 + ant_counts_7d_window2 - background_7d_ant_w1 - background_7d_ant_w2) + (post_counts_7d_window1 + post_counts_7d_window2 - background_7d_post_w1 - background_7d_post_w2)) / 2.
        
        ### results; add in label areas
        self.label_areaRetention_2.config(text=str(retention_2w))
        patdata['Retention 2-Fenster [%]'] = retention_2w
    
        dt_list, retention_10, retention_15 = retention_lists(counts_0d, T_75se)
        dt_selen, decay_selen = selen_decay(counts_0d, T_75se)

        ### plot
        ax.clear()
    
        ax.plot(dt_list, retention_10, label='Retention = 10%')
        ax.plot(dt_list, retention_15, label='Retention = 15%')
        ax.plot(7., counts_7d, 'o')
        ax.annotate('Retention', xy=(7.1, counts_7d))
        ax.axvline(x = 0, color='red', linestyle='--', linewidth='0.33')
        ax.axvline(x = 7, color='red', linestyle='--', linewidth='0.33')
        ax.set_ylabel('kcts')
        ax.set_xlabel('Tagen')
        ax.legend()


#%% start application

app = SeHCAT_eval()
app.mainloop()