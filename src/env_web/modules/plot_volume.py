import numpy as np
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap, Colormap
import matplotlib.pyplot as plt
from typing import Any


@st.fragment
def plot_volume(
    ax: plt.Axes,
    volume: np.ndarray,
    view: str,
    slice_index: int,
    colormap: Any,
    angle: int,
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


@st.fragment
def modify_colormap(cmap: Colormap) -> Colormap:
    colors = cmap(np.arange(cmap.N))  # Copy the colormap to modify it
    colors[0] = [0, 0, 0, 1]  # Set the first color (value 0) to black
    new_cmap = LinearSegmentedColormap.from_list(
        "modified_cmap", colors, cmap.N
    )  # Create a new colormap
    return new_cmap
