"""
Creation date of this program: march 2019
Author: L. Gardy
E-mail: ludovic.gardy@cnrs.fr
Encoding: UTF-8
"""
import os
import numpy as np
import nibabel as nib
from pydicom import dcmread

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
