"""
Creation date of this program: march 2019
Author: L. Gardy
E-mail: ludovic.gardy@cnrs.fr
Encoding: UTF-8
"""
import os

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QSizePolicy,
    QHBoxLayout, QFrame, QSlider)
from PyQt5 import (QtCore, QtGui)
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Ladybird_MRI_viz.load_volume import load_volume
from Ladybird_MRI_viz.plot_volume import plot_volume
from Ladybird_MRI_viz.widgets.custom_slider import custom_slider

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100, facecol = 'black', file_type = "", atlas_name = ""):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor(facecol)
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')
        self.file_type = file_type
        self.atlas_name = atlas_name

        self.volume = None
        self.slice_type = None
        self.current_slice = None
        self.rotation = None
        self.kernel = []

        super(MplCanvas, self).__init__(self.fig)

        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        #print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
        #        ('double' if event.dblclick else 'single', event.button,
        #        event.x, event.y, event.xdata, event.ydata))

        if event.dblclick and type(self.volume) != None and type(self.slice_type) != None and type(self.current_slice) != None:

            self.zoom_plot = Zoomed_window(self.volume, self.slice_type, self.current_slice, self.rotation, self.kernel, self.file_type, self.atlas_name)

class Zoomed_window(QWidget):
    '''
    Open a new simple window displaying a zoom of the View 1, 2 or 3 of the volume.
    '''

    def __init__(self, volume, slice_type, current_slice, rotation, kernel, file_type, atlas_name):
        super().__init__()
        # Add a << always stay on top of the screen >> Flag to the window
        #self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Window )

        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("Zoom on {}".format(slice_type))

        self.original_volume = volume
        self.volume = volume
        self.slice_type = slice_type
        self.current_slice = current_slice
        self.rotation = rotation
        self.kernel = kernel
        self.file_type = file_type
        self.atlas_name = atlas_name

        self.init_values()

        self.show()

    def init_values(self):
        # Def window size
        left = 300
        top = 200
        width = 700
        height = 700
        slider = custom_slider()

        ##### Main frame
        main_Frame = QFrame()
        main_layout = QVBoxLayout()
        main_Frame.setLayout(main_layout)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setGeometry(left, top, width, height)

        self.slider = QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setStyleSheet(slider)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(1)

        if self.slice_type == "View_1":
            self.slider.setRange(0, self.volume.shape[0] - 1)
            self.slider.setValue(self.current_slice)

        elif self.slice_type == "View_2":
            self.slider.setRange(0, self.volume.shape[1] - 1)
            self.slider.setValue(self.current_slice)

        elif self.slice_type == "View_3":
            self.slider.setRange(0, self.volume.shape[2] - 1)
            self.slider.setValue(self.current_slice)

        self.slider.valueChanged.connect(lambda:self.slider_fun())
        self.slider_fun()

        ##### Add Widgets to main frame
        main_layout.addWidget(self.canvas)
        main_layout.addWidget(self.slider)

        #--- Add main frame to global layout ---#
        GLOBAL_LAYOUT = QHBoxLayout()
        GLOBAL_LAYOUT.addWidget(main_Frame)

        self.setLayout(GLOBAL_LAYOUT)

    def slider_fun(self):

        self.canvas.fig.clear()
        self.canvas.axes = self.canvas.fig.add_subplot(111)
        self.canvas.axes.axis('off')
        img = plot_volume(self.rotation, self.volume, self.slice_type, self.slider.value(), self.canvas.axes, self.kernel, self.file_type, self.atlas_name)
        self.canvas.draw()
