from PyQt6.QtWidgets import QMessageBox
from PyQt6 import QtCore

def messageBox_popup(title, text, icon, cancel_option = True):
    msgBox = QMessageBox()
    msgBox.setWindowFlags(QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.WindowMinimizeButtonHint | QtCore.Qt.WindowType.WindowMaximizeButtonHint | QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)# | QtCore.Qt.Window )
    msgBox.setIcon(icon)
    msgBox.setWindowTitle(title)
    msgBox.setText(text)

    if cancel_option:
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    else:
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)

    user_answer = msgBox.exec()
    if user_answer == QMessageBox.StandardButton.Ok:
        print('Confirmed.')
    return(user_answer)
