import os

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from src.env_global.config.config import get_path
from src.env_global.modules.load_volume import load_volume
from src.env_web.config.config import page_config
from src.env_web.modules.plot_volume import modify_colormap, plot_volume
from src.env_web.modules.ui_components import display_sidebar
from src.env_web.modules.utils import resize_volume

# TODO: manage DICOM format (folder)


class Home:
    def __init__(self):
        self.init_types()
        self.path_dict = get_path()
        self = display_sidebar(self, page_config)

        self.container_1 = st.container()
        with self.container_1:
            self.load_ui()

    def init_types(self):
        self.downscale_factor: float
        self.file_type: str
        self.enable_downscale: bool

    def update_slider(self):
        max_slice_index = int(
            st.session_state.volume.shape[
                st.session_state.views[str(st.session_state.view)]
            ]
            * self.downscale_factor
        )
        st.session_state.slice_index = int(max_slice_index / 2)
        st.session_state.slice_index = st.sidebar.slider(
            "Slice",
            0,
            max_slice_index,
            st.session_state.slice_index,
            key="slice_slider",
        )

    def load_ui(self):
        # st.title(f"Selected view: {st.session_state.view.lower()}")

        uploaded_file = None
        if self.file_type == "nifti":
            uploaded_file = st.file_uploader("Upload NIfTI file", type=["nii", "gz"])
        elif self.file_type == "dicom":
            uploaded_file = st.file_uploader("Upload DICOM folder", type=["dcm"])
        elif "template" in str(self.file_type):
            fpath = os.path.join(self.path_dict["mri_examples"], "atlas")
            template_name = self.file_type.split("-")[-1]
            fpath = os.path.join(fpath, f"{template_name}.nii.gz")
            st.session_state.atlas_name = os.path.split(fpath)[-1].split(".")[0]
            if (
                st.session_state.volume is None
                or st.session_state.file_type != self.file_type
            ):
                st.session_state.volume = load_volume(fpath, self.file_type)
                st.session_state.file_type = self.file_type

        if uploaded_file:
            try:
                if st.session_state.uploaded_file_name != uploaded_file.name:
                    save_dir = ".buffer"  # Change this to your desired directory
                    os.makedirs(save_dir, exist_ok=True)
                    file_path = os.path.join(save_dir, uploaded_file.name)

                    with open(file_path, "wb") as out_file:
                        out_file.write(uploaded_file.getbuffer())

                    st.session_state.volume = load_volume(file_path, self.file_type)
                    st.session_state.uploaded_file_name = uploaded_file.name
                    st.session_state.file_type = self.file_type

                    # Vider le buffer de uploaded_file
                    uploaded_file.seek(0)
                    uploaded_file.truncate(0)
            except Exception as e:
                st.error(f"Error loading volume: {str(e)}")

        if self.enable_downscale and st.session_state.volume is not None:
            st.session_state.volume = resize_volume(
                st.session_state.volume, self.downscale_factor
            )

        if st.session_state.volume is not None:
            self.display_views()

    def display_views(self):
        self.update_slider()

        with st.sidebar:
            col1, col2 = st.columns(2)
            with col1:
                kernel = st.selectbox(
                    "Select Filter", ["None", "Sobel", "Log", "Square Root"]
                )
            with col2:
                # Prepare the colormap list
                colormap_list = ["gray", "Grays"] + [
                    cm for cm in plt.colormaps() if cm not in ["gray", "Grays"]
                ]
                colormap_name = st.selectbox("Select Colormap", colormap_list)

        # Update colormap only if a new colormap is selected
        if colormap_name != st.session_state.selected_colormap_name:
            st.session_state.colormap = modify_colormap(plt.get_cmap(colormap_name))
            st.session_state.selected_colormap_name = colormap_name

        with st.sidebar:
            st.text("Rotate Image")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("↩️ Rotate", key="rotate_left"):
                    st.session_state.angle = (st.session_state.angle - 45) % 360
            with col2:
                if st.button("Rotate ↪️", key="rotate_right"):
                    st.session_state.angle = (st.session_state.angle + 45) % 360

        if kernel == "Sobel":
            st.session_state.volume = np.sqrt(st.session_state.volume)
        elif kernel == "Log":
            st.session_state.volume = np.log(np.abs(st.session_state.volume))
        elif kernel == "Square Root":
            st.session_state.volume = np.sqrt(st.session_state.volume)

        fig, ax = plt.subplots(figsize=(10, 10))
        plot_volume(
            fig,
            ax,
            st.session_state.volume,
            st.session_state.view,
            st.session_state.slice_index,
            kernel,
            st.session_state.file_type,
            st.session_state.atlas_name,
            st.session_state.colormap,
            st.session_state.angle,
        )
        st.pyplot(fig)

        with st.expander("Thumbnails View"):
            st.write("""Click on the thumbnails to select a slice.""")
            self.display_thumbnail_view(kernel, st.session_state.colormap)

    @st.experimental_fragment
    def display_thumbnail_view(self, kernel, colormap):
        num_thumbnails = 5

        thumbnail_indices = np.linspace(
            0,
            st.session_state.volume.shape[st.session_state.views[st.session_state.view]]
            * self.downscale_factor
            - 1,
            num=num_thumbnails,
            dtype=int,
        )

        thumbnails = st.columns(num_thumbnails)
        for i, idx in enumerate(thumbnail_indices):
            with thumbnails[i]:
                fig, ax = plt.subplots(figsize=(4, 4))
                plot_volume(
                    fig,
                    ax,
                    st.session_state.volume,
                    st.session_state.view,
                    idx,
                    kernel,
                    st.session_state.file_type,
                    st.session_state.atlas_name,
                    colormap,
                    st.session_state.angle,
                )
                st.pyplot(fig)
                if st.button(f"Select Slice", key=f"select_{idx}"):
                    st.session_state.slice_index = idx
                    st.rerun()


if __name__ == "__main__":
    home = Home()
