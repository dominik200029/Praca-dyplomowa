from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget, QVBoxLayout
from PyQt5.uic import loadUi
from matplotlib import pyplot as plt


class Gui(QMainWindow):
    """
    A class representing the main GUI window.

    Attributes:
    - None
    """

    def __init__(self):
        """
        Initializes the Gui object.

        Parameters:
        - None
        """
        super().__init__()

        loadUi('gui.ui', self)  # loading .ui file to display GUI

    @staticmethod
    def update_label(label, text):
        """
        Updates the text content of a QLabel.

        Parameters:
        - label (QLabel): The QLabel to be updated.
        - text (str): The new text content.

        Returns:
        - None
        """
        label.setPlainText(text)

    @staticmethod
    def print_error(message):
        """
        Displays an error message in a QMessageBox.

        Parameters:
        - message (str): The error message to be displayed.

        Returns:
        - None
        """
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()

