import numpy as np
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap


@st.experimental_fragment
def plot_volume(
    fig, ax, volume, view, slice_index, kernel, file_type, atlas_name, colormap, angle
):
    ax.clear()  # Clear the previous plot
    if view == "Sagittal":
        img = np.rot90(volume[slice_index, :, :], k=angle // 45)
    elif view == "Frontal":
        img = np.rot90(volume[:, slice_index, :], k=angle // 45)
    elif view == "Axial":
        img = np.rot90(volume[:, :, slice_index], k=angle // 45)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.imshow(img, cmap=colormap)
    # ax.set_aspect("equal")
    # fig.set_size_inches(10, 10)
    # fig.canvas.draw()


@st.experimental_fragment
def modify_colormap(cmap):
    # Copy the colormap to modify it
    colors = cmap(np.arange(cmap.N))
    # Set the first color (value 0) to black
    colors[0] = [0, 0, 0, 1]
    # Create a new colormap
    new_cmap = LinearSegmentedColormap.from_list("modified_cmap", colors, cmap.N)
    return new_cmap
