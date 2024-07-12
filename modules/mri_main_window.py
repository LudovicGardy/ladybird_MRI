import os
import numpy as np
import traceback
import sys

from PyQt6.QtWidgets import (QWidget, QLabel, QApplication, QPushButton, QFrame, QFileDialog,
    QVBoxLayout, QMainWindow, QMenu, QSizePolicy, QHBoxLayout, QSlider, QStyle, QComboBox,
    QToolBar, QSpinBox, QMessageBox)
from PyQt6 import (QtCore, QtGui)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QCoreApplication

from modules.load_volume import load_volume
from modules.plot_volume import plot_volume
from modules.zoomed_window import MplCanvas, ExpandedCanvas
from modules.widgets.custom_slider import custom_slider
from modules.messageBox_popup import messageBox_popup

from modules.config_file import get_path
path_dict = get_path()

developper_mode_1 = True
developper_mode_2 = True

class Main_Win(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ladybird - Imagery widget")
        left = 75 ; top = 75 ; width = 900 ; height = 900

        self.setWindowIcon(QtGui.QIcon(os.path.join(path_dict["root"], "modules", "static", "mri.ico")))
        self.setGeometry(left, top, width, height)

        self.atlas_name = ""

        self.set_menu()
        self.set_toolbar()

    def display_window(self, file_type):
        ### Load json file (data info) and events folder (raw data parts)
        self.file_type = file_type

        if "template" not in file_type:
            fpath = path_dict["mri_examples"]
        elif "template" in file_type:
            fpath = os.path.join(path_dict["mri_examples"], "atlas")
            template_name  = file_type.split("-")[-1]
            fpath = os.path.join(fpath,"{}.nii.gz".format(template_name))
            self.atlas_name = os.path.split(fpath)[-1].split(".")[0]

        if "nifti" in file_type and "template" not in file_type.lower():
            fpath = QFileDialog.getOpenFileName(None, "Select a NIfTI file:", fpath, "NIfTI files (*.nii *nii.gz)")[0]
        elif "dicom" in file_type and "template" not in file_type.lower():
            fpath = QFileDialog.getExistingDirectory(None, 'Select a DICOM folder:', fpath, QFileDialog.ShowDirsOnly)

        try:
            self.init_MainWidget(fpath, file_type)
            self.show()
        except:
            var = traceback.format_exc()
            user_answer = messageBox_popup("Error", f"Did you load data? \n\n{var}", QMessageBox.Icon.Critical, cancel_option = False)

    def init_MainWidget(self, fpath, file_type):
        self.centWidget = MRI_widget(fpath, file_type)
        self.setCentralWidget(self.centWidget)
        self.init_plot()

    def set_menu(self):
        ### Set window menu
        menubar = self.menuBar()

        self.load_menu = QMenu('&Load data', self)
        menubar.addMenu(self.load_menu)

        self.load_sub_menu = QMenu('&Clinical MRI')
        self.load_sub_menu.addAction('&From NIfTI', lambda:self.display_window("nifti"))
        self.load_sub_menu.addAction('&From DICOM', lambda:self.display_window("dicom"))
        self.load_menu.addMenu(self.load_sub_menu)

        self.atlas = QMenu('&Atlas', self)
        self.atlas.addAction('&AAL', lambda:self.display_window("nifti-template-aal"))
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
        
    def set_toolbar(self):
        ##### Init toolbar #####
        toolbar = QToolBar("MRI Window Toolbar")
        toolbar.setIconSize(QtCore.QSize(32,32))
        self.addToolBar(toolbar)
        #self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)
        ##### /Init toolbar #####

        ##### Set buttons #####
        ### New button
        rotateLeft_button = QAction(QtGui.QIcon(os.path.join(path_dict["toolbar_icones"], "icons8-rotate-left-96.png")),
                                "Rotate left", self)
        rotateLeft_button.triggered.connect(self.rotateLeft_button_fun)
        #rotateLeft_button.setCheckable(True)
        toolbar.addAction(rotateLeft_button)

        ### New button
        rotateRight_button = QAction(QtGui.QIcon(os.path.join(path_dict["toolbar_icones"], "icons8-rotate-right-96.png")),
                                "Rotate right", self)
        rotateRight_button.triggered.connect(self.rotateRight_button_fun)
        #rotateRight_button.setCheckable(True)
        toolbar.addAction(rotateRight_button)

        ### New button
        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(1)
        self.spinbox.setMaximum(4)
        self.spinbox.setPrefix("View ")
        self.spinbox.setSuffix(" selected")
        self.spinbox.setSingleStep(1)
        self.spinbox.valueChanged.connect(self.value_changed)
        self.spinbox.textChanged.connect(self.value_changed_str)

        ### New button
        expandVew_button = QAction(QtGui.QIcon(os.path.join(path_dict["toolbar_icones"], "icons8-expand-96.png")),
                                "Expand view", self)
        expandVew_button.triggered.connect(self.call_centWidget_expandView_fun)
        #rotateRight_button.setCheckable(True)
        toolbar.addAction(expandVew_button)
        toolbar.addWidget(self.spinbox)

        toolbar.addWidget(QLabel("           "))
        toolbar.addSeparator()

        ### New button
        button1 = QAction(QtGui.QIcon(os.path.join(path_dict["toolbar_icones"], "icons8-restore-window-64.png")),
                                "Restore original", self)
        button1.triggered.connect(self.restore_original_image)
        #rotateRight_button.setCheckable(True)
        toolbar.addAction(button1)

        ### New button
        button2 = QAction(QtGui.QIcon(os.path.join(path_dict["toolbar_icones"], "icons8-statistics-64.png")),
                                "Sobel filter", self)
        button2.triggered.connect(lambda:self.contrast_button_fun("contour"))
        #rotateRight_button.setCheckable(True)
        toolbar.addAction(button2)

        ### New button
        button3 = QAction(QtGui.QIcon(os.path.join(path_dict["toolbar_icones"], "icons8-illumination-brightness-96.png")),
                                "Brightness", self)
        button3.triggered.connect(lambda:self.brightness_button_fun("log"))
        #rotateRight_button.setCheckable(True)
        toolbar.addAction(button3)
        ##### /Set buttons #####

    #######################################################################
    ###                       DEFINE CALLBACKS                          ###
    #######################################################################
    def call_centWidget_expandView_fun(self):
        try:
            self.centWidget.expandView_fun(self.spinbox.value())
        except:
            var = traceback.format_exc()
            user_answer = messageBox_popup("Error", var, QMessageBox.Icon.Critical, cancel_option = False)

    def init_plot(self):
        try:
            self.centWidget.img_view1 = plot_volume(self.centWidget.figure1_canvas, self.centWidget.volume, "View_1", self.centWidget.view1_Slider.value(), kernel = self.centWidget.kernel, file_type = self.file_type, atlas_name = self.atlas_name, rotation = self.centWidget.rotation_view1)
            self.centWidget.img_view2 = plot_volume(self.centWidget.figure2_canvas, self.centWidget.volume, "View_2", self.centWidget.view2_Slider.value(), kernel = self.centWidget.kernel, file_type = self.file_type, atlas_name = self.atlas_name, rotation = self.centWidget.rotation_view2)
            self.centWidget.img_view3 = plot_volume(self.centWidget.figure3_canvas, self.centWidget.volume, "View_3", self.centWidget.view3_Slider.value(), kernel = self.centWidget.kernel, file_type = self.file_type, atlas_name = self.atlas_name, rotation = self.centWidget.rotation_view3)
        except:
            var = traceback.format_exc()
            user_answer = messageBox_popup("Error", var, QMessageBox.Icon.Critical, cancel_option = False)

    def value_changed(self, i):
        print(i)

    def value_changed_str(self, s):
        print(s)

    def rotateRight_button_fun(self):
        try:
            if self.spinbox.value() == 1:
                self.centWidget.rotation_view1 +=1
                val = self.centWidget.view1_Slider.value()
            elif self.spinbox.value() == 2:
                self.centWidget.rotation_view2 +=1
                val = self.centWidget.view2_Slider.value()
            elif self.spinbox.value() == 3:
                self.centWidget.rotation_view3 +=1
                val = self.centWidget.view3_Slider.value()

            self.centWidget.slider_fun(val, anat_plan = f"View_{self.spinbox.value()}")
        except:
            var = traceback.format_exc()
            user_answer = messageBox_popup("Error", var, QMessageBox.Icon.Critical, cancel_option = False)

    def rotateLeft_button_fun(self):
        try:
            if self.spinbox.value() == 1:
                self.centWidget.rotation_view1 -=1
                val = self.centWidget.view1_Slider.value()
            elif self.spinbox.value() == 2:
                self.centWidget.rotation_view2 -=1
                val = self.centWidget.view2_Slider.value()
            elif self.spinbox.value() == 3:
                self.centWidget.rotation_view3 -=1
                val = self.centWidget.view3_Slider.value()

            self.centWidget.slider_fun(val, anat_plan = f"View_{self.spinbox.value()}")
        except:
            var = traceback.format_exc()
            user_answer = messageBox_popup("Error", var, QMessageBox.Icon.Critical, cancel_option = False)

    def restore_original_image(self):
        try:
            self.centWidget.kernel = []
            self.centWidget.volume = self.centWidget.original_volume

            self.centWidget.slider_fun(self.centWidget.view1_Slider.value(), anat_plan="View_1")
            self.centWidget.slider_fun(self.centWidget.view2_Slider.value(), anat_plan="View_2")
            self.centWidget.slider_fun(self.centWidget.view3_Slider.value(), anat_plan="View_3")

            try:
                self.centWidget.expanded_widget.close()
                print("Expanded canvas reinitialization.")
            except:
                print("Nothing to update.")
        except:
            var = traceback.format_exc()
            user_answer = messageBox_popup("Error", var, QMessageBox.Icon.Critical, cancel_option = False)

    def contrast_button_fun(self, contrast_volume):
        try:
            if contrast_volume == "original":
                self.centWidget.kernel = []
            elif contrast_volume == "sharp":
                kernel = [ [0,-1,0], [-1,5,-1], [0,-1,0] ]
                self.centWidget.kernel = kernel
            elif contrast_volume == "contour":
                self.centWidget.kernel = "sobel"

            self.centWidget.slider_fun(self.centWidget.view1_Slider.value(), anat_plan="View_1")
            self.centWidget.slider_fun(self.centWidget.view2_Slider.value(), anat_plan="View_2")
            self.centWidget.slider_fun(self.centWidget.view3_Slider.value(), anat_plan="View_3")

            try:
                self.centWidget.expanded_widget.close()
                print("Expanded canvas reinitialization.")
            except:
                print("Nothing to update.")
        except:
            var = traceback.format_exc()
            user_answer = messageBox_popup("Error", var, QMessageBox.Icon.Critical, cancel_option = False)

    def brightness_button_fun(self, brightness_volume):
        try:
            if brightness_volume == "original":
                self.centWidget.volume = self.centWidget.original_volume
            elif brightness_volume == "sqrt":
                self.centWidget.volume = np.sqrt(self.centWidget.original_volume)
            elif brightness_volume == "log":
                self.centWidget.volume = np.log(np.abs(self.centWidget.original_volume))

            self.centWidget.slider_fun(self.centWidget.view1_Slider.value(), anat_plan="View_1")
            self.centWidget.slider_fun(self.centWidget.view2_Slider.value(), anat_plan="View_2")
            self.centWidget.slider_fun(self.centWidget.view3_Slider.value(), anat_plan="View_3")

            try:
                self.centWidget.expanded_widget.close()
                print("Expanded canvas reinitialization.")
            except:
                print("Nothing to update.")
        except:
            var = traceback.format_exc()
            user_answer = messageBox_popup("Error", var, QMessageBox.Icon.Critical, cancel_option = False)

class MRI_widget(QWidget):
    def __init__(self, fpath, file_type):
        super().__init__()
        self.set_layout()

        self.file_type = file_type
        self.atlas_name = ""
        self.rotation_view1 = 1
        self.rotation_view2 = 1
        self.rotation_view3 = 1

        slider = custom_slider()

        #self.setStyleSheet("background-color: black;")
        self.volume = load_volume(fpath, file_type)

        self.original_volume = self.volume
        self.kernel = []
        self.file_type = file_type

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)

        self.fill_layout()

    def set_layout(self):
        #######################################################################
        ###                            LEVEL 1                              ###
        #######################################################################

        ##### Global Frame #####
        self.global_frame = QFrame()
        self.global_layout = QVBoxLayout()
        self.global_frame.setLayout(self.global_layout)
        self.global_layout.addWidget(self.global_frame)
        self.global_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        ##### /Global Frame #####

        #######################################################################
        ###                           LEVEL 2                               ###
        #######################################################################

        ##### Container 1 #####
        self.container_frame_1 = QFrame()
        self.container_layout_1 = QHBoxLayout()
        self.container_frame_1.setLayout(self.container_layout_1)
        self.container_layout_1.addWidget(self.container_frame_1)
        self.container_frame_1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if developper_mode_1:
            self.container_frame_1.setObjectName("container_frame_1")
            self.container_frame_1.setStyleSheet("QFrame#container_frame_1 {background: #666666; border: 2px solid #000000;}")

        #if not developper_mode_2:
        #    self.container_layout_1.setSpacing(0)
        #    self.container_layout_1.setContentsMargins(0, 0, 0, 0)
        ##### /Container 1 #####

        #######################################################################
        ###                           LEVEL 3                               ###
        #######################################################################

        ##### Container 1 #####
        self.container_frame_1_1 = QFrame()
        self.container_layout_1_1 = QVBoxLayout()
        self.container_frame_1_1.setLayout(self.container_layout_1_1)
        self.container_layout_1_1.addWidget(self.container_frame_1_1)
        self.container_frame_1_1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if developper_mode_1:
            self.container_frame_1_1.setObjectName("container_frame_1_1")
            self.container_frame_1_1.setStyleSheet("QFrame#container_frame_1_1 {background: #adadad; border: 2px solid #000000;}")

        #if not developper_mode_1:
        #    self.container_layout_1_1.setSpacing(0)
        #    self.container_layout_1_1.setContentsMargins(1, 1, 1, 1)
        ##### /Container 1 #####

        ##### Container 2 #####
        self.container_frame_1_2 = QFrame()
        self.container_layout_1_2 = QVBoxLayout()
        self.container_frame_1_2.setLayout(self.container_layout_1_2)
        self.container_layout_1_2.addWidget(self.container_frame_1_2)

        self.container_frame_1_2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if developper_mode_1:
            self.container_frame_1_2.setObjectName("container_frame_1_2")
            self.container_frame_1_2.setStyleSheet("QFrame#container_frame_1_2 {background: #adadad; border: 2px solid #000000;}")

        #if not developper_mode_1:
        #    self.container_layout_1_2.setSpacing(0)
        #    self.container_layout_1_2.setContentsMargins(1, 1, 1, 1)
        ##### /Container 2 #####

        #######################################################################
        ###                           LEVEL 4                               ###
        #######################################################################
        ##### Container 1_1_1 #####
        self.container_frame_1_1_1 = QFrame()
        self.container_layout_1_1_1 = QVBoxLayout()
        self.container_frame_1_1_1.setLayout(self.container_layout_1_1_1)
        self.container_layout_1_1_1.addWidget(self.container_frame_1_1_1)
        self.container_frame_1_1_1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if True:
            self.container_frame_1_1_1.setObjectName("container_frame_1_1_1")
            self.container_frame_1_1_1.setStyleSheet("QFrame#container_frame_1_1_1 {background: #ebebeb; border: 2px solid #000000;}")

        if not True:
            self.container_layout_1_1_1.setSpacing(0)
            self.container_layout_1_1_1.setContentsMargins(0, 0, 0, 0)
        ##### /Container 1_1_1 #####

        ##### Container 1_1_2 #####
        self.container_frame_1_1_2 = QFrame()
        self.container_layout_1_1_2 = QVBoxLayout()
        self.container_frame_1_1_2.setLayout(self.container_layout_1_1_2)
        self.container_layout_1_1_2.addWidget(self.container_frame_1_1_2)
        self.container_frame_1_1_2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if True:
            self.container_frame_1_1_2.setObjectName("container_frame_1_1_2")
            self.container_frame_1_1_2.setStyleSheet("QFrame#container_frame_1_1_2 {background: #ebebeb; border: 2px solid #000000;}")

        if not True:
            self.container_layout_1_1_2.setSpacing(0)
            self.container_layout_1_1_2.setContentsMargins(0, 0, 0, 0)
        ##### /Container 1_1_2 #####

        ##### Container 1_1_3 #####
        self.container_frame_1_1_3 = QFrame()
        self.container_layout_1_1_3 = QVBoxLayout()
        self.container_frame_1_1_3.setLayout(self.container_layout_1_1_3)
        self.container_layout_1_1_3.addWidget(self.container_frame_1_1_3)
        self.container_frame_1_1_3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if True:
            self.container_frame_1_1_3.setObjectName("container_frame_1_1_3")
            self.container_frame_1_1_3.setStyleSheet("QFrame#container_frame_1_1_3 {background: #ebebeb; border: 2px solid #000000;}")

        if not True:
            self.container_layout_1_1_3.setSpacing(0)
            self.container_layout_1_1_3.setContentsMargins(0, 0, 0, 0)
        ##### /Container 1_1_3 #####

        ##### Container 1_1_4 #####
        self.container_frame_1_1_4 = QFrame()
        self.container_layout_1_1_4 = QVBoxLayout()
        self.container_frame_1_1_4.setLayout(self.container_layout_1_1_4)
        self.container_layout_1_1_4.addWidget(self.container_frame_1_1_4)
        self.container_frame_1_1_4.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if True:
            self.container_frame_1_1_4.setObjectName("container_frame_1_1_4")
            self.container_frame_1_1_4.setStyleSheet("QFrame#container_frame_1_1_4 {background: #ebebeb; border: 2px solid #000000;}")

        if not True:
            self.container_layout_1_1_4.setSpacing(0)
            self.container_layout_1_1_4.setContentsMargins(0, 0, 0, 0)
        ##### /Container 1_1_4 #####

        #######################################################################
        ###                           LEVEL 5                               ###
        #######################################################################

        ##### Container 1_1_1_1 #####
        self.container_frame_1_1_1_1 = QFrame()
        self.container_layout_1_1_1_1 = QVBoxLayout()
        self.container_frame_1_1_1_1.setLayout(self.container_layout_1_1_1_1)
        self.container_layout_1_1_1_1.addWidget(self.container_frame_1_1_1_1)
        self.container_frame_1_1_1_1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.container_frame_1_1_1_1.setFixedHeight(50)

        if True:
            self.container_frame_1_1_1_1.setObjectName("container_frame_1_1_1_1")
            self.container_frame_1_1_1_1.setStyleSheet("QFrame#container_frame_1_1_1_1 {background: white; border: 2px solid #000000;}")

        if not True:
            self.container_layout_1_1_1_1.setSpacing(0)
            self.container_layout_1_1_1_1.setContentsMargins(0, 0, 0, 0)
        ##### /Container 1_1_1_1 #####

        ##### Container 1_1_1_2 #####
        self.container_frame_1_1_1_2 = QFrame()
        self.container_layout_1_1_1_2 = QVBoxLayout()
        self.container_frame_1_1_1_2.setLayout(self.container_layout_1_1_1_2)
        self.container_layout_1_1_1_2.addWidget(self.container_frame_1_1_1_2)
        self.container_frame_1_1_1_2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.container_frame_1_1_1_2.setFixedHeight(50)

        if True:
            self.container_frame_1_1_1_2.setObjectName("container_frame_1_1_1_2")
            self.container_frame_1_1_1_2.setStyleSheet("QFrame#container_frame_1_1_1_2 {background: white; border: 2px solid #000000;}")

        if not True:
            self.container_layout_1_1_1_2.setSpacing(0)
            self.container_layout_1_1_1_2.setContentsMargins(0, 0, 0, 0)
        ##### /Container 1_1_1_2 #####

        ##### Container 1_1_1_3 #####
        self.container_frame_1_1_1_3 = QFrame()
        self.container_layout_1_1_1_3 = QVBoxLayout()
        self.container_frame_1_1_1_3.setLayout(self.container_layout_1_1_1_3)
        self.container_layout_1_1_1_3.addWidget(self.container_frame_1_1_1_3)
        self.container_frame_1_1_1_3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.container_frame_1_1_1_3.setFixedHeight(50)

        if True:
            self.container_frame_1_1_1_3.setObjectName("container_frame_1_1_1_3")
            self.container_frame_1_1_1_3.setStyleSheet("QFrame#container_frame_1_1_1_3 {background: white; border: 2px solid #000000;}")

        if not True:
            self.container_layout_1_1_1_3.setSpacing(0)
            self.container_layout_1_1_1_3.setContentsMargins(0, 0, 0, 0)
        ##### /Container 1_1_1_3 #####

        ##### Container 1_1_1_4 #####
        self.container_frame_1_1_1_4 = QFrame()
        self.container_layout_1_1_1_4 = QVBoxLayout()
        self.container_frame_1_1_1_4.setLayout(self.container_layout_1_1_1_4)
        self.container_layout_1_1_1_4.addWidget(self.container_frame_1_1_1_4)
        self.container_frame_1_1_1_4.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.container_frame_1_1_1_4.setFixedHeight(50)


        if True:
            self.container_frame_1_1_1_4.setObjectName("container_frame_1_1_1_4")
            self.container_frame_1_1_1_4.setStyleSheet("QFrame#container_frame_1_1_1_4 {background: white; border: 2px solid #000000;}")

        if True:
            self.container_layout_1_1_1_4.setSpacing(0)
            self.container_layout_1_1_1_4.setContentsMargins(0, 0, 0, 0)
        ##### /Container 1_1_1_4 #####

    def fill_layout(self):

        #######################################################################
        ###                              LABELS                            ###
        #######################################################################
        label1 = QLabel("Sagital", self)
        label2 = QLabel("Frontal", self)
        label3 = QLabel("Axial", self)
        label4 = QLabel("", self)
        label1.setFont(QtGui.QFont("", 16, QtGui.QFont.Weight.Bold))
        label2.setFont(QtGui.QFont("", 16, QtGui.QFont.Weight.Bold))
        label3.setFont(QtGui.QFont("", 16, QtGui.QFont.Weight.Bold))
        label4.setFont(QtGui.QFont("", 16, QtGui.QFont.Weight.Bold))

        #######################################################################
        ###                              SLIDERS                            ###
        #######################################################################
        slider = custom_slider()

        self.view1_Slider = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.view1_Slider.setSingleStep(1)
        self.view1_Slider.setPageStep(1)
        self.view1_Slider.setRange(0, self.volume.shape[0] - 1)
        self.view1_Slider.setValue( int(self.volume.shape[0]/4) )
        self.view1_Slider.valueChanged.connect(lambda:self.slider_fun(self.view1_Slider.value(), anat_plan="View_1"))
        self.view1_Slider.setStyleSheet(slider)

        self.view2_Slider = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.view2_Slider.setSingleStep(1)
        self.view2_Slider.setPageStep(1)
        self.view2_Slider.setRange(0, self.volume.shape[1] - 1)
        self.view2_Slider.setValue( int(self.volume.shape[1]/4) )
        self.view2_Slider.valueChanged.connect(lambda:self.slider_fun(self.view2_Slider.value(), anat_plan="View_2"))
        self.view2_Slider.setStyleSheet(slider)

        self.view3_Slider = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.view3_Slider.setSingleStep(1)
        self.view3_Slider.setPageStep(1)
        self.view3_Slider.setRange(0, self.volume.shape[2] - 1)
        self.view3_Slider.setValue( int(self.volume.shape[2]/4) )
        self.view3_Slider.valueChanged.connect(lambda:self.slider_fun(self.view3_Slider.value(), anat_plan="View_3"))
        self.view3_Slider.setStyleSheet(slider)

        self.view4_Slider = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.view4_Slider.setSingleStep(1)
        self.view4_Slider.setPageStep(1)
        self.view4_Slider.setRange(0, self.volume.shape[0] - 1)
        self.view4_Slider.setValue( int(self.volume.shape[0]/4) )
        self.view4_Slider.setStyleSheet(slider)


        #######################################################################
        ###                              FIGURES                            ###
        #######################################################################

        self.figure1_canvas = MplCanvas(self, facecolor = '#000000')
        self.figure2_canvas = MplCanvas(self, facecolor = '#000000')
        self.figure3_canvas = MplCanvas(self, facecolor = '#000000')
        self.figure4_canvas = MplCanvas(self, facecolor = '#000000')

        self.figure1_canvas.fig.set_tight_layout(True)
        self.figure2_canvas.fig.set_tight_layout(True)
        self.figure3_canvas.fig.set_tight_layout(True)
        self.figure4_canvas.fig.set_tight_layout(True)

        #######################################################################
        ###                   ADD WIDGETS TO LAYOUT                         ###
        #######################################################################

        self.container_layout_1_1_1_1.addWidget(label1)
        self.container_layout_1_1_1_2.addWidget(label2)
        self.container_layout_1_1_1_3.addWidget(label3)
        self.container_layout_1_1_1_4.addWidget(label4)

        self.container_layout_1_1_1_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.container_layout_1_1_1_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.container_layout_1_1_1_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.container_layout_1_1_1_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        #######################################################################
        ###                         SET LAYOUT                              ###
        #######################################################################

        self.setLayout(self.global_layout)
        self.global_layout.addWidget(self.container_frame_1)
        self.container_layout_1.addWidget(self.container_frame_1_1)
        self.container_layout_1.addWidget(self.container_frame_1_2)
        self.container_layout_1_1.addWidget(self.container_frame_1_1_1)
        self.container_layout_1_1.addWidget(self.container_frame_1_1_2)
        self.container_layout_1_2.addWidget(self.container_frame_1_1_3)
        self.container_layout_1_2.addWidget(self.container_frame_1_1_4)

        self.container_layout_1_1_1.addWidget(self.container_frame_1_1_1_1)
        self.container_layout_1_1_1.addWidget(self.figure1_canvas)
        self.container_layout_1_1_1.addWidget(self.view1_Slider)

        self.container_layout_1_1_2.addWidget(self.container_frame_1_1_1_3)
        self.container_layout_1_1_2.addWidget(self.figure3_canvas)
        self.container_layout_1_1_2.addWidget(self.view3_Slider)

        self.container_layout_1_1_3.addWidget(self.container_frame_1_1_1_2)
        self.container_layout_1_1_3.addWidget(self.figure2_canvas)
        self.container_layout_1_1_3.addWidget(self.view2_Slider)

        self.container_layout_1_1_4.addWidget(self.container_frame_1_1_1_4)
        self.container_layout_1_1_4.addWidget(self.figure4_canvas)
        self.container_layout_1_1_4.addWidget(self.view4_Slider)


    #######################################################################
    ###                       DEFINE CALLBACKS                          ###
    #######################################################################
    def slider_fun(self, slider_val, anat_plan):
        if "Expanded" in anat_plan:
            self.img_view4 = plot_volume(self.expanded_widget.figure_canvas, self.volume, anat_plan.split("-")[1], slider_val, kernel = self.kernel, file_type = self.file_type, atlas_name = self.atlas_name, rotation = self.expanded_rotation)
        elif anat_plan == "View_1":
            self.img_view1 = plot_volume(self.figure1_canvas, self.volume, anat_plan, slider_val, kernel = self.kernel, file_type = self.file_type, atlas_name = self.atlas_name, rotation = self.rotation_view1)
        elif anat_plan == "View_2":
            self.img_view2 = plot_volume(self.figure2_canvas, self.volume, anat_plan, slider_val, kernel = self.kernel, file_type = self.file_type, atlas_name = self.atlas_name, rotation = self.rotation_view2)
        elif anat_plan == "View_3":
            self.img_view3 = plot_volume(self.figure3_canvas, self.volume, anat_plan, slider_val, kernel = self.kernel, file_type = self.file_type, atlas_name = self.atlas_name, rotation = self.rotation_view3)

    def expandView_fun(self, spinbox_val):
        anat_plan = f"View_{spinbox_val}"

        slider = custom_slider()
        self.view5_Slider = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.view5_Slider.setSingleStep(1)
        self.view5_Slider.setPageStep(1)
        self.view5_Slider.setRange(0, self.volume.shape[0] - 1)
        self.view5_Slider.setValue( int(self.volume.shape[0]/4) )
        self.view5_Slider.setStyleSheet(slider)

        self.expanded_widget = ExpandedCanvas()
        self.expanded_widget.main_layout.addWidget(self.view5_Slider)

        if anat_plan == "View_1":
            self.img_view_expanded = plot_volume(self.expanded_widget.figure_canvas, self.volume, anat_plan, self.view5_Slider.value(), kernel = self.kernel, file_type = self.file_type, atlas_name = self.atlas_name, rotation = self.rotation_view1)
            self.view5_Slider.valueChanged.connect(lambda:self.slider_fun(self.view5_Slider.value(), f"Expanded-{anat_plan}"))
            self.expanded_rotation =  self.rotation_view1
        elif anat_plan == "View_2":
            self.img_view_expanded = plot_volume(self.expanded_widget.figure_canvas, self.volume, anat_plan, self.view5_Slider.value(), kernel = self.kernel, file_type = self.file_type, atlas_name = self.atlas_name, rotation = self.rotation_view2)
            self.view5_Slider.valueChanged.connect(lambda:self.slider_fun(self.view5_Slider.value(), f"Expanded-{anat_plan}"))
            self.expanded_rotation =  self.rotation_view2
        elif anat_plan == "View_3":
            self.img_view_expanded = plot_volume(self.expanded_widget.figure_canvas, self.volume, anat_plan, self.view5_Slider.value(), kernel = self.kernel, file_type = self.file_type, atlas_name = self.atlas_name, rotation = self.rotation_view3)
            self.view5_Slider.valueChanged.connect(lambda:self.slider_fun(self.view5_Slider.value(), f"Expanded-{anat_plan}"))
            self.expanded_rotation =  self.rotation_view3

        self.expanded_widget.show()
        #self.figure5_canvas_expanded = MplCanvas(None, facecolor = '#000000')
        #self.expanded_widget.draw()
