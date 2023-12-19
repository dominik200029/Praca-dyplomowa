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


def print_error(message):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(message)
    msg.exec_()


class AxisHandler:
    def __init__(self, data):
        self.samples_number = data['samples_number']
        self.sampling_frequency = data['sampling_frequency']
        self.time_step = data['time_step']

    def generate_time_axis(self):
        time_axis = np.arange(0, (self.samples_number - 1) / self.sampling_frequency, self.time_step)
        return time_axis

    def generate_frequency_axis(self, signal):
        fft_x_axis = fftfreq(len(signal), 1 / self.sampling_frequency)
        return fft_x_axis


class Signal:
    def __init__(self, amplitude, frequency, phase):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def calculate_sine_wave(self, time):
        signal = self.amplitude * np.sin(2 * np.pi * self.frequency * time + self.phase)
        return signal


class FFTAnalyzer:
    def __init__(self, signal):
        self.signal = signal

    def calculate_fft(self, data):
        axis = AxisHandler(data)
        fft_x_axis = axis.generate_frequency_axis(self.signal)
        fft_data = fft(self.signal)
        return fft_x_axis, fft_data

    def calculate_ifft(self):
        return ifft(self.signal)


class View(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi('gui.ui', self)

        self.canvas_dict = {
            'signal': Canvas(self.layout1),
            'fft': Canvas(self.layout2),
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
    def __init__(self):
        self.signals_amount = 0
        self.signals = []

    def add_signal(self, data):
        self.signals.append(Signal(data['amplitude'][self.signals_amount], data['frequency'][self.signals_amount],
                                   data['phase'][self.signals_amount]))
        self.signals_amount += 1

    def generate_wave(self, data):
        axis = AxisHandler(data)
        time_axis = axis.generate_time_axis()
        wave = np.zeros(len(time_axis))

        for signal in self.signals:
            wave += signal.amplitude * np.sin(2 * np.pi * signal.frequency * time_axis + signal.phase)

        return time_axis, wave

    def generate_fft(self, axis_data):
        wave = self.generate_wave(axis_data)[1]
        fft_analyzer = FFTAnalyzer(wave)
        fft_axis, fft_data = fft_analyzer.calculate_fft(axis_data)
        return fft_axis, fft_data

    def generate_ifft(self, fft_function):
        fft_analyzer = FFTAnalyzer(fft_function)
        ifft_data = fft_analyzer.calculate_ifft()
        return np.real(ifft_data)


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.amplitude = []
        self.frequency = []
        self.phase = []

    def collect_signal_data(self):
        amplitude_text = self.view.amplitude_edit.text()
        frequency_text = self.view.frequency_edit.text()
        phase_text = self.view.phase_edit.text()

        if not (amplitude_text and frequency_text and phase_text):
            print_error("Wprowadz wszystkie dane")
            return None

        self.amplitude.append(float(amplitude_text))
        self.frequency.append(float(frequency_text))
        self.phase.append(float(phase_text))

        data = {
            'amplitude': self.amplitude,
            'frequency': self.frequency,
            'phase': self.phase
        }
        return data

    def collect_axis_data(self):
        time_step_text = self.view.time_step_edit.text()
        sampling_frequency_text = self.view.sampling_fr_edit.text()
        samples_number_text = self.view.samples_number_edit.text()

        if not (time_step_text and sampling_frequency_text and samples_number_text):
            print_error("Wprowadz wszystkie dane")
            return None

        time_step = float(time_step_text)
        sampling_frequency = float(sampling_frequency_text)
        samples_number = float(samples_number_text)

        data = {
            'time_step': time_step,
            'sampling_frequency': sampling_frequency,
            'samples_number': samples_number
        }
        return data

    def handle_update_button(self):
        self.view.clear_canvas()
        data = self.collect_axis_data()
        time_axis, wave = self.model.generate_wave(data)
        self.view.update_canvas('signal', time_axis, wave, 'Original signal', 'plot', 'Time',
                                'Amplitude')
        fft_x_data, fft_data = self.model.generate_fft(data)
        self.view.update_canvas('fft', fft_x_data, abs(fft_data), 'abs(FFT)', 'stem', 'Frequency',
                                'Magnitude')
        ifft_data = self.model.generate_ifft(fft_data)
        self.view.update_canvas('ifft', time_axis, np.real(ifft_data), 'Inverse FFT', 'plot', 'Time',
                                'Amplitude')

    def handle_add_button(self):
        data = self.collect_signal_data()
        self.model.add_signal(data)


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
