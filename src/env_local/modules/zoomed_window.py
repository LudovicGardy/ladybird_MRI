"""
Creation date of this program: march 2019
Author: L. Gardy
E-mail: ludovic.gardy@cnrs.fr
Encoding: UTF-8
"""
import os

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6 import QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from src.env_global.config.config import get_path

class MplCanvas(FigureCanvas):
    '''
    Figure Canvas that is inserted for each view in main window and in
    expanded (autonmous) window.
    '''

    def __init__(self, parent=None, width=5, height=4, dpi=100, facecolor = '#f0f0f0', linewidth = 0, edgecolor = "black"):

        super().__init__()

        #self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig = plt.figure(figsize=(width, height), dpi=dpi, linewidth = linewidth, edgecolor = edgecolor)#, constrained_layout=True)
        self.fig.patch.set_facecolor(facecolor)
        #self.fig.set_tight_layout(True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding)
        FigureCanvas.updateGeometry(self)

        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                ('double' if event.dblclick else 'single', event.button,
                event.x, event.y, event.xdata, event.ydata))

class ExpandedCanvas(QWidget):
    '''
    Create a new autonomus window (QWidget) in which the figure canvas
    is inserted, where user click the "expand button" in the
    toolbar of the main window.
    '''
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Expanded view")
        self.setWindowIcon(QtGui.QIcon(get_path()["mri.ico"]))

        self.main_layout = QVBoxLayout()

        self.figure_canvas = MplCanvas(self, facecolor = "black")
        self.main_layout.addWidget(self.figure_canvas)

        self.setLayout(self.main_layout)
