"""
Creation date of this program: march 2019
Author: L. Gardy
E-mail: ludovic.gardy@cnrs.fr
Encoding: UTF-8
"""
import os

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import imageio
import nibabel as nib
from pydicom import dcmread
import cv2


def load_volume(folderpath, file_type):

    # init
    volume = None

    if file_type == "dicom":

        # Get file names into the images folder
        file_list = os.listdir(folderpath)

        # Read each 2D image and save it into a list
        allimages_list = []

        for file_name in file_list:

            ds = dcmread(folderpath + "/" + file_name)
            allimages_list.append(ds.pixel_array)

        volume = np.array(allimages_list)

    elif "nifti" in file_type:
        v = nib.load(folderpath)
        volume = v.get_fdata()

        # remove 4rd dimension (time) if exists because we are not watching
        #- dynamic images
        if len(volume.shape) >= 4:
            volume = volume[:,:,:,0]

    else:

        print(os.path.split(folderpath)[0], "is not an imagery file. Not added to the volume.")

    if type(volume) != type(None):
        print("Volume dimensions", volume.shape)

    return(volume)

def plot_volume(rotation, volume, slice_type, n_slice, ax= [], kernel = [], file_type = "", atlas_name = ""):

    #rotation = 0

    if not ax:

        f, ax = plt.subplots()

    if slice_type == "View_3":
        #img = np.rot90(volume[:, :, n_slice],rotation)
        img = volume[:, :, n_slice]
    elif slice_type == "View_2":
        #img = np.rot90(volume[:, n_slice, :],rotation)
        img = volume[:, n_slice, :]
    elif slice_type == "View_1":
        #img = np.rot90(volume[n_slice, :, :],rotation)
        img = volume[n_slice, :, :]

    img = np.rot90(img,rotation)

    if len(kernel) > 0:
        if type(kernel) == list or type(kernel) == np.ndarray:
            img = ndimage.filters.convolve(img, kernel, mode='nearest')
            img[img < 0] = 0
        elif kernel == "sobel":
            #img = cv2.Sobel(img, cv2.CV_8U, 1, 1, ksize = 1)
            sobel_x = ndimage.filters.convolve(img, np.array([ [-1,0,1], [-2,0,2], [-1,0,1] ]), mode='nearest')
            sobel_y = ndimage.filters.convolve(img, np.array([ [-1,-2,-1], [0,0,0], [1,2,1] ]), mode='nearest')
            img = np.sqrt( sobel_x**2 + sobel_y**2 )

    if "template" in file_type and "ch2" not in atlas_name and "inia19" not in atlas_name:
        clist = ["#000000" ,"#a6cee3", "#1f78b4","#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"]
        cmap = matplotlib.colors.ListedColormap(clist)
    else:
        cmap = plt.cm.gray

    ax.imshow(img, interpolation='nearest', cmap=cmap, aspect = 'auto')
    ax.axis('off')

    return(img)
