"""
Creation date of this program: march 2019
Author: L. Gardy
E-mail: ludovic.gardy@cnrs.fr
Encoding: UTF-8
"""
import os
import numpy as np
import traceback
import sys

from PyQt5.QtWidgets import (QWidget, QLabel, QApplication, QPushButton, QFrame, QFileDialog,
    QVBoxLayout, QMainWindow, QMenu, QSizePolicy, QHBoxLayout, QSlider, QStyle, QComboBox)
from PyQt5 import (QtCore, QtGui)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

from Ladybird_MRI_viz.load_volume import load_volume
from Ladybird_MRI_viz.plot_volume import plot_volume
from Ladybird_MRI_viz.zoomed_window import MplCanvas

from Ladybird_MRI_viz.widgets.custom_slider import custom_slider

class Main_Win(QMainWindow):
    """
    This class displays the main window of the program, with the menu.
    At initialization, user can load data, that will be displayed
    among 3 planes (cube), using the customWidget (QWidget) class.

    Parameters
    ----------
    inheritance: QMainWindow
        PyQt5.QtWidgets.QMainWindow
    """

    def __init__(self):
        super().__init__()

        ### Set window parameters
        left = 200
        top = 100
        width = 700
        height = 800
        self.setGeometry(left, top, width, height)
        self.default_backgroundColor = self.palette().color(QtGui.QPalette.Background).name()

        ### Set window menu
        self.load_menu = QMenu('&Load data', self)
        self.menuBar().addMenu(self.load_menu)
        self.load_sub_menu = QMenu('&Clinical MRI')
        self.load_sub_menu.addAction('&From NIfTI', lambda:self.display_window("nifti"))
        self.load_sub_menu.addAction('&From DICOM', lambda:self.display_window("dicom"))
        self.load_menu.addMenu(self.load_sub_menu)
        self.atlas = QMenu('&Atlas',self)
        self.atlas.addAction('&AAL', lambda:self.display_window("nifti-template-aal"))
        self.atlas.addAction('&AAL3', lambda:self.display_window("nifti-template-AAL3v1_for_SPM12"))
        self.atlas.addAction('&AICHAmc', lambda:self.display_window("nifti-template-AICHAmc"))
        self.atlas.addAction('&Brodmann', lambda:self.display_window("nifti-template-brodmann"))
        self.atlas.addAction('&Ch2', lambda:self.display_window("nifti-template-ch2"))
        self.atlas.addAction('&Ch2bet', lambda:self.display_window("nifti-template-ch2bet"))
        self.atlas.addAction('&Ch2better', lambda:self.display_window("nifti-template-ch2better"))
        self.atlas.addAction('&HarvardOxford', lambda:self.display_window("nifti-template-HarvardOxford_cort_maxprob_thr0_1mm"))
        self.atlas.addAction('&Inia19-NeuroMaps', lambda:self.display_window("nifti-template-inia19_NeuroMaps"))
        self.atlas.addAction('&Inia19-T1', lambda:self.display_window("nifti-template-inia19_t1_brain"))
        self.atlas.addAction('&JHU-WhiterMatter-1mm', lambda:self.display_window("nifti-template-JHU_WhiteMatter_labels_1mm"))
        self.atlas.addAction('&JHU-WhiterMatter-2mm', lambda:self.display_window("nifti-template-JHU_WhiteMatter_labels_2mm"))
        self.atlas.addAction('&Natbrainlab', lambda:self.display_window("nifti-template-natbrainlab"))
        self.load_menu.addMenu(self.atlas)

    def display_window(self, file_type):
        ### Load json file (data info) and events folder (raw data parts)
        file_type = file_type.lower()

        if "template" not in file_type:
            fpath = "~"
        elif "template" in file_type:
            current_script_directory = os.path.dirname(os.path.realpath('__file__'))
            fpath =  os.path.join(current_script_directory, "Ladybird_MRI_viz", "examples", "atlas")
            template_name  = file_type.split("-")[-1]
            fpath = os.path.join(fpath,"{}.nii.gz".format(template_name))

        if "nifti" in file_type and "template" not in file_type:
            fpath = QFileDialog.getOpenFileName(None, "Select a NIfTI file:", fpath, "NIfTI files (*.nii *nii.gz)")[0]
        elif "dicom" in file_type and "template" not in file_type:
            fpath = QFileDialog.getExistingDirectory(None, 'Select a DICOM folder:', fpath, QFileDialog.ShowDirsOnly)

        try:
            ### Set Central Widget
            self.MRIviz_centWidget = customWidget(fpath, file_type)
            self.setCentralWidget(self.MRIviz_centWidget)
        except:
            var = traceback.format_exc()
            print(var)

class customWidget(QWidget):
    """
    This class is called by Main_Win (QMainWindow) once user have selected
    the data, to display the images in 3 planes.
    A parameter frame will also be created with some buttons so that user can
    apply images processing features.

    Parameters
    ----------
    inheritance: QWidget
        PyQt5.QtWidgets.QWidget

    fpath: str
        If nifti: filepath
        If DICOM: folderpath

    file_type: str
        "nifti" or "dicom"
    """
    def __init__(self, fpath, file_type):

        super().__init__()
        self.file_type = file_type
        self.fpath = fpath
        self.atlas_name = ""
        slider = custom_slider()

        self.setStyleSheet("background-color: black;")
        self.volume = load_volume(self.fpath, file_type)
        self.original_volume = self.volume
        self.kernel = []
        self.file_type = file_type

        self.rotations_pos = [0,3,2,1]
        self.rotations_idx = -1
        self.rotation_view1 = self.rotations_pos[self.rotations_idx]
        self.rotation_view2 = self.rotations_pos[self.rotations_idx]
        self.rotation_view3 = self.rotations_pos[self.rotations_idx]

        if "ct" in self.fpath.lower():
            self.brightness_button_fun("Sqrt")

        if "template" in file_type:
            self.atlas_name = os.path.split(self.fpath)[-1].split(".")[0]

        current_script_directory = os.path.dirname(os.path.realpath('__file__'))
        icones_folderpath = os.path.join(current_script_directory, "ladybird/icones/32x32").replace("\\", "/")

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)

        ### Main frame
        main_Frame = QFrame()
        main_layout = QVBoxLayout()
        main_Frame.setLayout(main_layout)

        ### Frontal / Sagittal view frame
        fs_Frame = QFrame()
        fs_Layout = QHBoxLayout()
        fs_Frame.setLayout(fs_Layout)

        ##- Frontal view frame
        view1_Frame = QFrame()
        view1_Layout = QVBoxLayout()
        view1_Frame.setLayout(view1_Layout)
        view1_Frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        view1_label = QLabel()

        if "nifti" in file_type.lower():
            view1_label.setText("Anat. plan 1")
        else:
            view1_label.setText("Plan 1")

        view1_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        view1_label.setFixedHeight(50)
        view1_label.setFont(QtGui.QFont("", 20, QtGui.QFont.Bold))
        view1_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        view1_label.setStyleSheet("background-color: black; color : white")

        self.view1_Canvas = MplCanvas(self, width=5, height=4, dpi=100, file_type = self.file_type, atlas_name = self.atlas_name)
        self.view1_Canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view1_Canvas.volume = self.volume
        self.view1_Canvas.rotation = self.rotation_view1

        self.view1_Slider = QSlider(QtCore.Qt.Horizontal, self)
        self.view1_Slider.setTickPosition(QSlider.NoTicks)
        self.view1_Slider.setSingleStep(1)
        self.view1_Slider.setPageStep(1)
        self.view1_Slider.setRange(0, self.volume.shape[0] - 1)
        self.view1_Slider.setValue( int(self.volume.shape[0]/4) )
        self.view1_Slider.valueChanged.connect(lambda:self.slider_fun("View_1"))
        self.slider_fun("View_1")
        self.view1_Slider.setStyleSheet(slider)

        view1_Layout.addWidget(view1_label)
        view1_Layout.addWidget(self.view1_Canvas)
        view1_Layout.addWidget(self.view1_Slider)

        ##- Sagital view frame
        view2_Frame = QFrame()
        view2_Layout = QVBoxLayout()
        view2_Frame.setLayout(view2_Layout)
        view2_Frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        view2_label = QLabel()

        if "nifti" in file_type.lower():
            view2_label.setText("Anat. plan 2")
        else:
            view2_label.setText("Pan 2")

        view2_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        view2_label.setFixedHeight(50)
        view2_label.setFont(QtGui.QFont("", 20, QtGui.QFont.Bold))
        view2_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        view2_label.setStyleSheet("background-color: black; color : white")

        self.view2_Canvas = MplCanvas(self, width=5, height=4, dpi=100, file_type = self.file_type, atlas_name = self.atlas_name)
        self.view2_Canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view2_Canvas.volume = self.volume
        self.view2_Canvas.rotation = self.rotation_view2

        self.view2_Slider = QSlider(QtCore.Qt.Horizontal, self)
        self.view2_Slider.setSingleStep(1)
        self.view2_Slider.setPageStep(1)
        self.view2_Slider.setRange(0, self.volume.shape[1] - 1)
        self.view2_Slider.setValue( int(self.volume.shape[1]/4) )
        self.view2_Slider.valueChanged.connect(lambda:self.slider_fun("View_2"))
        self.slider_fun("View_2")
        self.view2_Slider.setStyleSheet(slider)

        view2_Layout.addWidget(view2_label)
        view2_Layout.addWidget(self.view2_Canvas)
        view2_Layout.addWidget(self.view2_Slider)

        fs_Layout.addWidget(view1_Frame)
        fs_Layout.addWidget(view2_Frame)

        ### Axial view & param box
        tp_Frame = QFrame()
        tp_Layout = QHBoxLayout()
        tp_Frame.setLayout(tp_Layout)

        ##- Axial view frame
        view3_Frame = QFrame()
        view3_Layout = QVBoxLayout()
        view3_Frame.setLayout(view3_Layout)
        view3_Frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        view3_label = QLabel()

        if "nifti" in file_type.lower():
            view3_label.setText("Anat. plan 3")
        else:
            view3_label.setText("Plan 3")

        view3_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        view3_label.setFixedHeight(50)
        view3_label.setFont(QtGui.QFont("", 20, QtGui.QFont.Bold))
        view3_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        view3_label.setStyleSheet("background-color: black; color : white")

        self.view3_Canvas = MplCanvas(self, width=5, height=4, dpi=100, file_type = self.file_type, atlas_name = self.atlas_name)
        self.view3_Canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view3_Canvas.volume = self.volume
        self.view3_Canvas.rotation = self.rotation_view3

        self.view3_Slider = QSlider(QtCore.Qt.Horizontal, self)
        self.view3_Slider.setSingleStep(1)
        self.view3_Slider.setPageStep(1)
        self.view3_Slider.setRange(0, self.volume.shape[2] - 1)
        self.view3_Slider.setValue( int(self.volume.shape[2]/4) )
        self.view3_Slider.valueChanged.connect(lambda:self.slider_fun("View_3"))
        self.slider_fun("View_3")
        self.view3_Slider.setStyleSheet(slider)

        view3_Layout.addWidget(view3_label)
        view3_Layout.addWidget(self.view3_Canvas)
        view3_Layout.addWidget(self.view3_Slider)

        ##- Sagital view frame
        param_Frame = QFrame()
        param_Layout = QVBoxLayout()
        param_Frame.setLayout(param_Layout)
        param_Frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        param_Frame.setObjectName("param_Frame")
        param_Frame.setStyleSheet("QFrame#param_Frame {background: white ;border: 4px solid grey;}")

        param_label = QLabel()
        param_label.setText("Parameters")
        param_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        param_label.setFont(QtGui.QFont("", 20, QtGui.QFont.Bold))
        param_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        param_label.setStyleSheet("background-color: white; color: black")

        param_Canvas = MplCanvas(self, width=5, height=4, dpi=100, facecol = 'white')

        brightness_Frame = QFrame()
        brightness_Layout = QVBoxLayout()
        brightness_Frame.setLayout(brightness_Layout)
        brightness_Frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        brightness_Frame.setStyleSheet("background-color: white; color : black")

        brightness_buttonframe = QFrame()
        brightness_buttonlayout = QHBoxLayout()
        brightness_buttonframe.setLayout(brightness_buttonlayout)
        brightness_buttonframe.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        brightness_buttonframe.setFixedHeight(50)

        brightness_label = QLabel()
        brightness_label.setText("Brightness level")
        brightness_label.setFont(QtGui.QFont("12", 12, QtGui.QFont.Bold))

        brightness1_button = QPushButton("Original", self)
        brightness1_button.clicked.connect(lambda: self.brightness_button_fun("Original"))
        brightness1_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        brightness2_button = QPushButton("Sqrt", self)
        brightness2_button.clicked.connect(lambda: self.brightness_button_fun("Sqrt"))
        brightness2_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        brightness3_button = QPushButton("Log", self)
        brightness3_button.clicked.connect(lambda: self.brightness_button_fun("Log"))
        brightness3_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        brightness1_button.setStyleSheet("QPushButton { background-color: lightgrey; color: black }"
                            "QPushButton:pressed { background-color: black; color: lightgrey }" )
        brightness2_button.setStyleSheet("QPushButton { background-color: lightgrey; color: black }"
                            "QPushButton:pressed { background-color: black; color: lightgrey }" )
        brightness3_button.setStyleSheet("QPushButton { background-color: lightgrey; color: black }"
                            "QPushButton:pressed { background-color: black; color: lightgrey }" )

        brightness_buttonlayout.addWidget(brightness1_button)
        brightness_buttonlayout.addWidget(brightness2_button)
        brightness_buttonlayout.addWidget(brightness3_button)

        brightness_Layout.addWidget(brightness_label)
        brightness_Layout.addWidget(brightness_buttonframe)

        contrast_Frame = QFrame()
        contrast_Layout = QVBoxLayout()
        contrast_Frame.setLayout(contrast_Layout)
        contrast_Frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        contrast_Frame.setStyleSheet("background-color: white; color : black")

        contrast_buttonframe = QFrame()
        contrast_buttonlayout = QHBoxLayout()
        contrast_buttonframe.setLayout(contrast_buttonlayout)
        contrast_buttonframe.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        contrast_buttonframe.setFixedHeight(50)

        contrast_label = QLabel()
        contrast_label.setText("Contrast level")
        contrast_label.setFont(QtGui.QFont("12", 12, QtGui.QFont.Bold))

        contrast1_button = QPushButton("Original", self)
        contrast1_button.clicked.connect(lambda: self.contrast_button_fun("Original"))
        contrast1_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        contrast2_button = QPushButton("Sharp", self)
        contrast2_button.clicked.connect(lambda: self.contrast_button_fun("Sharp"))
        contrast2_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        contrast3_button = QPushButton("Contour", self)
        contrast3_button.clicked.connect(lambda: self.contrast_button_fun("Contour"))
        contrast3_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        contrast1_button.setStyleSheet("QPushButton { background-color: lightgrey; color: black }"
                            "QPushButton:pressed { background-color: black; color: lightgrey }" )
        contrast2_button.setStyleSheet("QPushButton { background-color: lightgrey; color: black }"
                            "QPushButton:pressed { background-color: black; color: lightgrey }" )
        contrast3_button.setStyleSheet("QPushButton { background-color: lightgrey; color: black }"
                            "QPushButton:pressed { background-color: black; color: lightgrey }" )

        contrast_buttonlayout.addWidget(contrast1_button)
        contrast_buttonlayout.addWidget(contrast2_button)
        contrast_buttonlayout.addWidget(contrast3_button)

        contrast_Layout.addWidget(contrast_label)
        contrast_Layout.addWidget(contrast_buttonframe)

        rotation_Frame = QFrame()
        rotation_Layout = QVBoxLayout()
        rotation_Frame.setLayout(rotation_Layout)
        rotation_Frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        rotation_Frame.setStyleSheet("background-color: white; color : black")

        rotation_buttonframe = QFrame()
        rotation_buttonlayout = QHBoxLayout()
        rotation_buttonframe.setLayout(rotation_buttonlayout)
        rotation_buttonframe.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        rotation_buttonframe.setFixedHeight(50)

        rotation_label = QLabel()
        rotation_label.setText("Image rotation")
        rotation_label.setFont(QtGui.QFont("12", 12, QtGui.QFont.Bold))

        self.rotation_comboBox = QComboBox()
        self.rotation_comboBox.addItem("View 1")
        self.rotation_comboBox.addItem("View 2")
        self.rotation_comboBox.addItem("View 3")
        self.rotation_comboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        iconfile = os.path.join(icones_folderpath, "Rotate left.png")
        rotation2_button = QPushButton("", self)
        rotation2_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        rotation2_button.clicked.connect(self.rotateLeft_button_fun)
        rotation2_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        iconfile = os.path.join(icones_folderpath, "Rotate right.png")
        rotation3_button = QPushButton("", self)
        rotation3_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        rotation3_button.clicked.connect(self.rotateRight_button_fun)
        rotation3_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.rotation_comboBox.setStyleSheet("QPushButton { background-color: lightgrey; color: black }"
                            "QPushButton:pressed { background-color: black; color: lightgrey }" )
        rotation2_button.setStyleSheet("QPushButton { background-color: lightgrey; color: black }"
                            "QPushButton:pressed { background-color: black; color: lightgrey }" )
        rotation3_button.setStyleSheet("QPushButton { background-color: lightgrey; color: black }"
                            "QPushButton:pressed { background-color: black; color: lightgrey }" )

        rotation_buttonlayout.addWidget(self.rotation_comboBox)
        rotation_buttonlayout.addWidget(rotation2_button)
        rotation_buttonlayout.addWidget(rotation3_button)

        rotation_Layout.addWidget(rotation_label)
        rotation_Layout.addWidget(rotation_buttonframe)

        param_Layout.addWidget(param_label)
        param_Layout.addWidget(brightness_Frame)
        param_Layout.addWidget(contrast_Frame)
        param_Layout.addWidget(rotation_Frame)

        tp_Layout.addWidget(view3_Frame)
        tp_Layout.addWidget(param_Frame)

        ### Add Widgets to main frame
        main_layout.addWidget(fs_Frame)
        main_layout.addWidget(tp_Frame)

        #--- Add main frame to global layout ---#
        GLOBAL_LAYOUT = QHBoxLayout()
        GLOBAL_LAYOUT.addWidget(main_Frame)

        self.setLayout(GLOBAL_LAYOUT)

    def slider_fun(self, slice_type):
        if slice_type == "View_1":
            self.view1_Canvas.fig.clear()
            self.view1_Canvas.axes = self.view1_Canvas.fig.add_subplot(111)
            self.view1_Canvas.axes.axis('off')
            img = plot_volume(self.rotation_view1, self.volume,slice_type,self.view1_Slider.value(), self.view1_Canvas.axes, self.kernel, self.file_type, self.atlas_name)

            self.view1_Canvas.slice_type = slice_type
            self.view1_Canvas.current_slice = self.view1_Slider.value()

            self.view1_Canvas.draw()

        elif slice_type == "View_2":
            self.view2_Canvas.fig.clear()
            self.view2_Canvas.axes = self.view2_Canvas.fig.add_subplot(111)
            self.view2_Canvas.axes.axis('off')
            img = plot_volume(self.rotation_view2, self.volume,slice_type,self.view2_Slider.value(), self.view2_Canvas.axes, self.kernel, self.file_type, self.atlas_name)

            self.view2_Canvas.slice_type = slice_type
            self.view2_Canvas.current_slice = self.view2_Slider.value()

            self.view2_Canvas.draw()

        elif slice_type == "View_3":
            self.view3_Canvas.fig.clear()
            self.view3_Canvas.axes = self.view3_Canvas.fig.add_subplot(111)
            self.view3_Canvas.axes.axis('off')
            img = plot_volume(self.rotation_view3, self.volume,slice_type,self.view3_Slider.value(), self.view3_Canvas.axes, self.kernel, self.file_type, self.atlas_name)

            self.view3_Canvas.slice_type = slice_type
            self.view3_Canvas.current_slice = self.view3_Slider.value()

            self.view3_Canvas.draw()

    def rotateRight_button_fun(self):
        self.rotations_idx += 1

        if self.rotations_idx > 3:
            self.rotations_idx = 0

        if self.rotation_comboBox.currentText() == "View 1":
            self.rotation_view1 = self.view1_Canvas.rotation = self.rotations_pos[self.rotations_idx]
        elif self.rotation_comboBox.currentText() == "View 2":
            self.rotation_view2 = self.view2_Canvas.rotation = self.rotations_pos[self.rotations_idx]
        elif self.rotation_comboBox.currentText() == "View 3":
            self.rotation_view3 = self.view3_Canvas.rotation = self.rotations_pos[self.rotations_idx]

        self.slider_fun("View_3")
        self.slider_fun("View_2")
        self.slider_fun("View_1")

    def rotateLeft_button_fun(self):
        self.rotations_idx -= 1

        if self.rotations_idx < 0:
            self.rotations_idx = 3

        if self.rotation_comboBox.currentText() == "View 1":
            self.rotation_view1 = self.view1_Canvas.rotation = self.rotations_pos[self.rotations_idx]
        elif self.rotation_comboBox.currentText() == "View 2":
            self.rotation_view2 = self.view2_Canvas.rotation = self.rotations_pos[self.rotations_idx]
        elif self.rotation_comboBox.currentText() == "View 3":
            self.rotation_view3 = self.view3_Canvas.rotation = self.rotations_pos[self.rotations_idx]

        self.slider_fun("View_3")
        self.slider_fun("View_2")
        self.slider_fun("View_1")

    def contrast_button_fun(self, contrast_volume):
        if contrast_volume == "Original":
            self.kernel = []
        elif contrast_volume == "Sharp":
            kernel = [ [0,-1,0], [-1,5,-1], [0,-1,0] ]
            self.kernel = kernel
        elif contrast_volume == "Contour":
            self.kernel = "sobel"

        ### Send new volume to canvas object for zoom window
        self.view1_Canvas.kernel = self.kernel
        self.view3_Canvas.kernel = self.kernel
        self.view2_Canvas.kernel = self.kernel

        self.slider_fun("View_3")
        self.slider_fun("View_2")
        self.slider_fun("View_1")

    def brightness_button_fun(self, brightness_volume):
        if brightness_volume == "Original":
            self.volume = self.original_volume
        elif brightness_volume == "Sqrt":
            self.volume = np.sqrt(self.original_volume)
        elif brightness_volume == "Log":
            self.volume = np.log(self.original_volume)

        ### Send new volume to canvas object for zoom window
        self.view1_Canvas.volume = self.volume
        self.view3_Canvas.volume = self.volume
        self.view2_Canvas.volume = self.volume

        self.slider_fun("View_3")
        self.slider_fun("View_2")
        self.slider_fun("View_1")
