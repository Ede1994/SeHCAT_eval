# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 10:44:23 2021

@author: Eric
"""
import pydicom
import os
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

PathDicom = 'C:/Users/Eric/Documents/GitHub/SeHCAT_eval/Examples/SeHCAT_GE670/'
lstFilesDCM = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName,filename))
            
print(lstFilesDCM)

# Get dcm file
dcm_file = pydicom.read_file(lstFilesDCM[0])

np_pixel_array = dcm_file.pixel_array
#print(np_pixel_array)

print('Ant_EM1:', numpy.sum(np_pixel_array[0]))
print('Post_EM1:', numpy.sum(np_pixel_array[1]))
print('Ant_EM2:', numpy.sum(np_pixel_array[2]))
print('Post_EM2:', numpy.sum(np_pixel_array[3]))
#print(np_pixel_array[0].shape)


# plot of all WBs
fig, axes = plt.subplots(2,2, figsize=(10,10))

# the data
data_list = [np_pixel_array[0], np_pixel_array[1], np_pixel_array[2], np_pixel_array[3]]

# the names
name_list = ['Ant_EM1', 'Post_EM1', 'Ant_EM2', 'Post_EM2']

for ax, name, data in zip(axes.flatten(), name_list, data_list):
    im = ax.imshow(data, aspect='auto')             # plot data with default colormap
    ax.yaxis.set_major_locator(plt.NullLocator())   # remove y axis ticks
    ax.xaxis.set_major_locator(plt.NullLocator())   # remove x axis ticks
    ax.set_aspect('equal', adjustable='box')        # make subplots square
    ax.set_title(f'Cmap: {name}', fontsize=18)      # add a title to each
    divider = make_axes_locatable(ax)               # make colorbar same size as each subplot
    cax = divider.append_axes("right", size="5%", pad=0.1)
    plt.colorbar(im, cax=cax)

plt.show()