from typing import Callable

import matplotlib.pyplot as plt
import streamlit as st

from src.env_web.modules.plot_volume import modify_colormap


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def init_page_config(page_config: Callable):
    st.set_page_config(
        page_title=page_config().get("page_title"),
        page_icon=page_config().get("page_icon"),
        layout=page_config().get("layout"),
        initial_sidebar_state=page_config().get("initial_sidebar_state"),
    )


def init_session_state():
    st.session_state.views = {"Sagittal": 0, "Frontal": 1, "Axial": 2}

    if "slice_index" not in st.session_state:
        st.session_state.slice_index = 0
    if "angle" not in st.session_state:
        st.session_state.angle = 45
    if "volume" not in st.session_state:
        st.session_state.volume = None
    if "file_type" not in st.session_state:
        st.session_state.file_type = ""
    if "atlas_name" not in st.session_state:
        st.session_state.atlas_name = ""
    if "uploaded_file_name" not in st.session_state:
        st.session_state.uploaded_file_name = None
    if "colormap" not in st.session_state:
        st.session_state.colormap = modify_colormap(plt.get_cmap("gray"))
    if "selected_colormap_name" not in st.session_state:
        st.session_state.selected_colormap_name = "gray"
    if "view" not in st.session_state:
        st.session_state.view = "Sagittal"


def display_sidebar(self, page_config: Callable):
    with st.sidebar:
        col1, col2 = st.columns([1, 3])

        with col1:
            st.image(str(page_config().get("page_logo")), width=60)
        with col2:
            st.write("# 3D Med Viewer")

        st.caption(str(page_config().get("page_description")))

        st.divider()

    st.sidebar.title("Import data")

    self.file_type = st.sidebar.selectbox(
        "Data Type Selection",
        [
            "nifti",
            "dicom",
            "nifti-template-aal",
            "nifti-template-AICHAmc",
            "nifti-template-brodmann",
            "nifti-template-ch2",
            "nifti-template-ch2bet",
            "nifti-template-ch2better",
            "nifti-template-HarvardOxford_cort_maxprob_thr0_1mm",
            "nifti-template-inia19_NeuroMaps",
            "nifti-template-inia19_t1_brain",
            "nifti-template-JHU_WhiteMatter_labels_1mm",
            "nifti-template-JHU_WhiteMatter_labels_2mm",
            "nifti-template-natbrainlab",
        ],
    )

    self.enable_downscale = st.sidebar.checkbox("Enable Image Downscale", value=False)
    self.downscale_factor = (
        st.sidebar.slider("Downscale Factor", 0.1, 1.0, 0.5)
        if self.enable_downscale
        else 1.0
    )

    st.sidebar.title("View Controls")

    st.session_state.view = st.sidebar.radio(
        "Select View", ["Sagittal", "Frontal", "Axial"]
    )

    return self
