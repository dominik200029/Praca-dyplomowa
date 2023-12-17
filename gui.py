import sys
import numpy as np
import sympy as sp

from scipy.fft import fft, ifft, dct, idct

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUi

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('gui.ui', self)  # wczytanie pliku UI z QtDesignera

        # inicjalizacja wykresów
        self.canvas1 = FigureCanvas(Figure(figsize=(5, 5)))
        self.signalPlot_layout.addWidget(NavigationToolbar(self.canvas1, self))
        self.signalPlot_layout.addWidget(self.canvas1)
        self.ax1 = self.canvas1.figure.subplots()

        self.canvas2 = FigureCanvas(Figure(figsize=(5, 5)))
        self.sampledSignal_layout.addWidget(NavigationToolbar(self.canvas2, self))
        self.sampledSignal_layout.addWidget(self.canvas2)
        self.ax2 = self.canvas2.figure.subplots()

        self.canvas3 = FigureCanvas(Figure(figsize=(5, 5)))
        self.reconstructedSignal_layout.addWidget(NavigationToolbar(self.canvas3, self))
        self.reconstructedSignal_layout.addWidget(self.canvas3)
        self.ax3 = self.canvas3.figure.subplots()

        self.pushButton.clicked.connect(self.update)

    # funkcja wywoływana za każdym razem, kiedy naciśniemy przycisk 'Update'
    def update(self):
        amplitude_text = self.amplitude_edit.text()
        frequency_text = self.frequency_edit.text()
        t_max_text = self.signal_duration_edit.text()
        fs_text = self.sampling_fr_edit.text()
        timeStep_text = self.timeStep_edit.text()
        phase_text = self.phase_edit.text()

        # jeżeli nic nie wpiszemy w pola tekstowe -> okienko z błedem
        if not amplitude_text or not frequency_text or not t_max_text or not fs_text or not phase_text:
            self.printError("Wprowadź wszystkie dane")
            return

        # pobranie wartości, jeżeli podamy coś innego niz liczbę - błąd
        try:
            amplitude = float(amplitude_text)
            frequency = float(frequency_text)
            t_max = float(t_max_text)
            fs = float(fs_text)
            timeStep = float(timeStep_text)
            phase = float(sp.sympify(phase_text))
        except (ValueError, sp.SympifyError):
            self.printError("Podaj poprawną wartość")
            return

        # oś czasu
        t = np.arange(0, t_max, timeStep)
        y = 0
        y_text = ""

        if self.sine_radioButton.isChecked():
            y = y + amplitude * np.sin(2 * np.pi * frequency * t + phase)
            y_text = y_text + str(amplitude) + "sin(2π" + str(frequency) + " + " + str(phase) + ")"
        else:
            y = 0

        self.plot_signal_graph(self.ax1, "Wykres sygnału", t, y)
        self.plotDCT(self.ax3, "DCT", y)
        self.signal_label.setText(y_text)

    def plot_signal_graph(self, ax, title, t, y):
        ax.clear()
        ax.plot(t, y)
        ax.set_xlabel('Time')
        ax.set_ylabel('Amplitude')
        ax.set_title(title)
        ax.figure.canvas.draw()

    def plotFFT(self, ax, title, ys):
        ax.clear()
        Y = fft(ys)
        ax.stem(abs(Y))
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Magnitude')
        ax.set_title(title)
        ax.figure.canvas.draw()

    def plotDCT(self, ax, title, y):
        ax.clear()
        Y = dct(y)
        ax.stem(abs(Y))
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Magnitude')
        ax.set_title(title)
        ax.figure.canvas.draw()

    def printError(self, message):
        msg = QMessageBox()
        msg.setWindowTitle("Value Error")
        msg.setText(message)
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())
