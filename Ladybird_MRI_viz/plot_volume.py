import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import imageio
import cv2
from scipy import ndimage

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
