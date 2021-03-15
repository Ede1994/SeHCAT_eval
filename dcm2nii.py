# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 10:44:23 2021

@author: Eric
"""
import pydicom
import os
import numpy
import matplotlib.pyplot as plt

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
print(np_pixel_array)

print(numpy.sum(np_pixel_array))
print(np_pixel_array[0].shape)

fig = plt.figure(figsize=(6, 3.2))

ax = fig.add_subplot(111)
ax.set_title('colorMap')
plt.imshow(np_pixel_array[0])
ax.set_aspect('equal')

cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
cax.get_xaxis().set_visible(False)
cax.get_yaxis().set_visible(False)
cax.patch.set_alpha(0)
cax.set_frame_on(False)
plt.colorbar(orientation='vertical')
plt.show()
