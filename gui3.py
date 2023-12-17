import sys
import numpy as np

from scipy.fft import fft, ifft, dct, idct, fftshift, fftfreq

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUi

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Canvas:
    def __init__(self, layout):
        self.figure = Figure(figsize=(5, 5))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(NavigationToolbar(self.canvas, None))
        layout.addWidget(self.canvas)
        self.ax = self.figure.subplots()

    def plot(self, x, y, title, plot_type, x_label, y_label):
        #  self.ax.clear()
        if plot_type == 'stem':
            self.ax.stem(x, y)
        elif plot_type == 'plot':
            self.ax.plot(x, y)
        else:
            raise Exception('Plot type can be either "plot" or "stem"')
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(title)
        self.ax.figure.canvas.draw()

    def clear_canvas(self):
        self.ax.clear()


class SamplingHandler:
    def __init__(self, samples_number, sampling_frequency, time_step):
        self.samples_number = samples_number
        self.sampling_frequency = sampling_frequency
        self.time_step = time_step

    def generate_time_axis(self):
        time_axis = np.arange(0, (self.samples_number - 1) / self.sampling_frequency, self.time_step)
        return time_axis


class Signal:
    def __init__(self, amplitude, frequency, phase, samples_number, sampling_frequency, time_step):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    #    self.samples_number = samples_number
    #    self.sampling_frequency = sampling_frequency
    #    self.time_step = time_step
    #    self.time_axis = []

    def generate_sine_wave(self, time):
        signal = self.amplitude * np.sin(2 * np.pi * self.frequency * time + self.phase)
        return signal


class FFTAnalyzer:
    def __init__(self, signal: Signal):
        self.signal = signal

    def calculate_fft(self):
        pass


class View(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi('gui.ui', self)

        self.canvas_dict = {
            'signal': Canvas(self.layout1),
            'dft': Canvas(self.layout2),
            'ifft': Canvas(self.layout3),
            'dct': Canvas(self.layout4),
            'idct': Canvas(self.layout5)
        }

    def update_canvas(self, canvas_type, x, y, title, plot_type, x_label, y_label):
        canvas = self.canvas_dict.get(canvas_type)
        if canvas:
            canvas.plot(x, y, title, plot_type, x_label, y_label)

    def clear_canvas(self):
        for canvas in self.canvas_dict.values():
            if canvas:
                canvas.clear_canvas()


class Model:
    def generate_signal(self, amplitude, frequency, phase, samples_number, sampling_frequency, time_step):
        signal = Signal(amplitude, frequency, phase, samples_number, sampling_frequency, time_step)
        sampling_parameters = SamplingHandler(samples_number, sampling_frequency, time_step)
        time_axis = sampling_parameters.generate_time_axis()
        y_data = signal.generate_sine_wave(time_axis)
        return y_data, time_axis


def print_error(message):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(message)
    msg.exec_()


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.y_data = np.array([])  # Initialize as an empty NumPy array
        self.time_axis = np.array([])  # Initialize as an empty NumPy array

    def collect_data(self):
        amplitude_text = self.view.amplitude_edit.text()
        frequency_text = self.view.frequency_edit.text()
        phase_text = self.view.phase_edit.text()
        time_step_text = self.view.time_step_edit.text()
        sampling_frequency_text = self.view.sampling_fr_edit.text()
        samples_number_text = self.view.samples_number_edit.text()

        if not (amplitude_text and frequency_text and
                sampling_frequency_text and phase_text and samples_number_text):
            print_error("Wprowadź wszystkie dane")
            return None

        amplitude = float(amplitude_text)
        frequency = float(frequency_text)
        phase = float(phase_text)
        time_step = float(time_step_text)
        sampling_frequency = float(sampling_frequency_text)
        samples_number = float(samples_number_text)

        data = {
            'amplitude': amplitude,
            'frequency': frequency,
            'phase': phase,
            'time_step': time_step,
            'sampling_frequency': sampling_frequency,
            'samples_number': samples_number
        }
        return data

    def handle_update_button(self):
        # clean all canvases
        self.view.clear_canvas()

        # Update signal's canvas
        self.view.update_canvas('signal', self.time_axis, self.y_data,
                                'Sum of Signals', 'plot', 'Time', 'Amplitude')

    def handle_add_button(self):
        data = self.collect_data()
        generated_wave, time_axis = self.model.generate_signal(data['amplitude'], data['frequency'], data['phase'],
                                                               data['samples_number'], data['sampling_frequency'],
                                                               data['time_step'])

        if not self.y_data.size:
            self.y_data = generated_wave
            self.time_axis = time_axis
        else:
            # Ensure the dimensions match before concatenating
            if len(self.y_data) == len(generated_wave):
                self.y_data = np.add(self.y_data, generated_wave)
            else:
                print_error("Error: Dimensions mismatch. Cannot add signals.")


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        self.model = Model()
        self.view = View()
        self.controller = Controller(self.model, self.view)
        self.view.update_button.clicked.connect(self.controller.handle_update_button)
        self.view.add_button.clicked.connect(self.controller.handle_add_button)
        self.view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
