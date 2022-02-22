"""
Creation date of this program: march 2019
Author: L. Gardy
E-mail: ludovic.gardy@cnrs.fr
Encoding: UTF-8
"""
import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QApplication)

from Ladybird_MRI_viz.main_window import Main_Win

if __name__ == "__main__":
    # Avoid python kernel from dying
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # run
    mywindow = Main_Win()
    mywindow.show()
    sys.exit(app.exec_())
