# -*- coding: utf-8 -*-
"""
Created on Tue May 18 13:24:09 2021

@author: Eric
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import os
import pydicom
import numpy as np
from datetime import date

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


# get today's date
today = date.today().strftime("%d/%m/%Y")

### Fonts
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


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


English:
Please fill in all fields accordingly. Note: Data in kilo-counts!
Press the 'Berechnen!'-Button to get the final retention in %.
"""), font=NORM_FONT)
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


# read dcm header to dictionary
def dcm2header(filename, patdata):
    dcm_header = pydicom.dcmread(filename)
    patdata['Name'] = str(dcm_header[0x0054, 0x0400].value)
    patdata['Birthday'] = str(dcm_header[0x0010, 0x0030].value[6:8] + '.' + dcm_header[0x0010, 0x0030].value[4:6] + '.' + dcm_header[0x0010, 0x0030].value[0:4])
    patdata['Height'] = str(float(dcm_header[0x0010, 0x1020].value)*100)
    patdata['Weight'] = str(dcm_header[0x0010, 0x1030].value)


# read dcm data to numpy array
def dcm2data(filename):
    # read dicom file
    dcm_file = pydicom.read_file(filename)

    # convert to array
    np_pixel_array = dcm_file.pixel_array
        
    ant_w1 = float(np.sum(np_pixel_array[0]) / 1000)
    post_w1 = float(np.sum(np_pixel_array[1]) / 1000)
    ant_w2 = float(np.sum(np_pixel_array[2]) / 1000)
    post_w2 = float(np.sum(np_pixel_array[3]) / 1000)
    
    return ant_w1, post_w1, ant_w2, post_w2


# save button; pdf printout
def SaveData(fig, patdata):    
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
    save.drawString(480,750, str(today))
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
    #save.drawString(30,460, "Unterschrift MPE:")
    #save.line(125,457,320,457)
    
    # draw image
    imgdata = BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data

    Image = ImageReader(imgdata)
    save.drawImage(Image, 75, 200, 450, 230)

    # save pdf file
    save.showPage()
    save.save()
    
    # remove tmp files
    os.remove(filename)
