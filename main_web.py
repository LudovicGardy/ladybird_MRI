import os
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from src.env_global.modules.load_volume import load_volume
from src.env_global.config.config import get_path
from src.env_web.config.config import page_config
from src.env_web.modules.plot_volume import plot_volume, modify_colormap
from src.env_web.modules.utils import resize_volume

# TODO: manage DICOM format (folder)

### Set the page configuration
st.set_page_config(
    page_title="3D Med Viewer",
    page_icon=page_config().get("page_icon"),
    layout="wide",  # 'centered' or 'wide'
    initial_sidebar_state="expanded",  # 'expanded', 'collapsed', or 'auto'
)


### Set up the CSS style
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css(get_path()["styles.css"])

st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    """,
    unsafe_allow_html=True
)
### Main class for the imagery widget
class ImageryWidget:
    def __init__(self):
        st.session_state.views = {"Sagittal": 0, "Frontal": 1, "Axial": 2}
        self.path_dict = get_path()
        self.steup_sidebar()
        self.init_session_state()

        self.container_1 = st.container()
        with self.container_1:
            self.load_ui()

    def init_session_state(self):
        if 'slice_index' not in st.session_state:
            st.session_state.slice_index = 0
        if 'angle' not in st.session_state:
            st.session_state.angle = 45
        if 'volume' not in st.session_state:
            st.session_state.volume = None
        if 'file_type' not in st.session_state:
            st.session_state.file_type = ""
        if 'atlas_name' not in st.session_state:
            st.session_state.atlas_name = ""
        if 'uploaded_file_name' not in st.session_state:
            st.session_state.uploaded_file_name = None
        if 'colormap' not in st.session_state:
            st.session_state.colormap = modify_colormap(plt.get_cmap("gray"))
        if 'selected_colormap_name' not in st.session_state:
            st.session_state.selected_colormap_name = "gray"
        if 'view' not in st.session_state:
            st.session_state.view = "Sagittal"

    def steup_sidebar(self):

        with st.sidebar:

            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.image(str(page_config().get('page_logo')), width=60)
            with col2:
                st.write('# 3D Med Viewer')

            st.caption(str(page_config().get('page_description')))

            st.divider()

        st.sidebar.title("Import data")

        self.file_type = st.sidebar.selectbox("Data Type Selection", ["nifti", "dicom", "nifti-template-aal", "nifti-template-AICHAmc", 
                                                                   "nifti-template-brodmann", "nifti-template-ch2", "nifti-template-ch2bet", 
                                                                   "nifti-template-ch2better", "nifti-template-HarvardOxford_cort_maxprob_thr0_1mm", 
                                                                   "nifti-template-inia19_NeuroMaps", "nifti-template-inia19_t1_brain", 
                                                                   "nifti-template-JHU_WhiteMatter_labels_1mm", "nifti-template-JHU_WhiteMatter_labels_2mm", 
                                                                   "nifti-template-natbrainlab"])
        
        self.enable_downscale = st.sidebar.checkbox("Enable Image Downscale", value=False)
        self.downscale_factor = st.sidebar.slider("Downscale Factor", 0.1, 1.0, 0.5) if self.enable_downscale else 1.0

        st.sidebar.title("View Controls")

        st.session_state.view = st.sidebar.radio("Select View", ["Sagittal", "Frontal", "Axial"])

    def update_slider(self):
        max_slice_index = int(st.session_state.volume.shape[st.session_state.views[str(st.session_state.view)]] * self.downscale_factor)
        st.session_state.slice_index = int(max_slice_index / 2)
        st.session_state.slice_index = st.sidebar.slider("Slice", 0, max_slice_index, st.session_state.slice_index, key="slice_slider")

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
            if st.session_state.volume is None or st.session_state.file_type != self.file_type:
                st.session_state.volume = load_volume(fpath, self.file_type)
                st.session_state.file_type = self.file_type

        if uploaded_file:
            try:
                if st.session_state.uploaded_file_name != uploaded_file.name:
                    save_dir = ".buffer"  # Change this to your desired directory
                    os.makedirs(save_dir, exist_ok=True)
                    file_path = os.path.join(save_dir, uploaded_file.name)
                    
                    with open(file_path, 'wb') as out_file:
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
            st.session_state.volume = resize_volume(st.session_state.volume, self.downscale_factor)

        if st.session_state.volume is not None:
            self.display_views()

    def display_views(self):

        self.update_slider()

        with st.sidebar:
            col1, col2 = st.columns(2)
            with col1:
                kernel = st.selectbox("Select Filter", ["None", "Sobel", "Log", "Square Root"])
            with col2:
                # Prepare the colormap list
                colormap_list = ["gray", "Grays"] + [cm for cm in plt.colormaps() if cm not in ["gray", "Grays"]]
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
        plot_volume(fig, ax, st.session_state.volume, st.session_state.view, st.session_state.slice_index, kernel, st.session_state.file_type, st.session_state.atlas_name, st.session_state.colormap, st.session_state.angle)
        st.pyplot(fig)

        with st.expander("Thumbnails View"):
            st.write('''Click on the thumbnails to select a slice.''')
            self.display_thumbnail_view(kernel, st.session_state.colormap)

    def display_thumbnail_view(self, kernel, colormap):
        num_thumbnails = 5
        
        thumbnail_indices = np.linspace(0, st.session_state.volume.shape[st.session_state.views[st.session_state.view]] * self.downscale_factor - 1, num=num_thumbnails, dtype=int)

        thumbnails = st.columns(num_thumbnails)
        for i, idx in enumerate(thumbnail_indices):
            with thumbnails[i]:
                fig, ax = plt.subplots(figsize=(4, 4))
                plot_volume(fig, ax, st.session_state.volume, st.session_state.view, idx, kernel, st.session_state.file_type, st.session_state.atlas_name, colormap, st.session_state.angle)
                st.pyplot(fig)
                if st.button(f"Select Slice", key=f"select_{idx}"):
                    st.session_state.slice_index = idx
                    st.rerun()

if __name__ == "__main__":
    ImageryWidget()
