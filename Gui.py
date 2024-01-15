# View class represents the main GUI window
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from Canvas import Canvas

""" Class responsible for handling the look of user interface """


class Gui(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi('gui.ui', self)  # loading .ui file to display GUI

        # Dictionary to hold Canvas instances for different plots
        self.canvas_dict = {
            'signal': Canvas(self.layout1),
            'fft': Canvas(self.layout2),
            'ifft': Canvas(self.layout3),
            'dct': Canvas(self.layout4),
            'idct': Canvas(self.layout5)
        }

    def update_canvas(self, canvas_type, x, y, title, plot_type, x_label, y_label):
        """ Update the specified canvas
            x - Horizontal Axis Data
            y - Vertical Axis Data
            title - name shown on the top of a plot
            plot_type - plot for continuous-time plotting
                        stem for discrete-time plotting
            x_label - name shown as X axis title
            y_label - name shown as Y axis title """
        canvas = self.canvas_dict.get(canvas_type)
        #  check if chosen canvas exists
        if canvas:
            canvas.plot(x, y, title, plot_type, x_label, y_label)

    def clear_all(self):
        """ Clear all plots """
        for canvas in self.canvas_dict.values():
            if canvas:
                canvas.clear_canvas()

    def update_signals_label(self, signals_labels):
        """ updates text in signal label field"""
        text = ''
        for signal_label in signals_labels:
            text += signal_label
        self.signal_label.setPlainText(text)

    @staticmethod
    def print_error(message):
        """ Display an error message in a pop-up dialog """
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()
