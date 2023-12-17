import sys
import numpy as np

from scipy.fft import fft, ifft, dct, idct, fftshift, fftfreq

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUi

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


def print_error(message):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(message)
    msg.exec_()


# klasa sterująca logiką pomiędzy innymi klasami
class MainModel:
    def __init__(self):
        self.signal = None
        self.total_wave = None

    # self.signal_fft = None

    def create_signal(self, amplitude, frequency, phase):
        self.signal = Signal(amplitude, frequency, phase)

    def add_signal(self):
        self.total_wave = self.total_wave + self.signal

    def get_fft_data(self):
        return self.signal.generate_fft()

    def get_ifft_data(self):
        return self.signal.generate_ifft()

    def get_dct_data(self):
        return self.signal.generate_dct()

    def get_idct_data(self):
        return self.signal.generate_idct()


# klasa odpowiadająca za wygląd GUI
class MainView(QMainWindow):
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


# klasa odpowiadająca za stworzenie jednego sygnału sinusoidalnego
class Signal:
    def __init__(self, amplitude, frequency, phase):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    #  self.duration = duration
    #   self.time_step = time_step
    # self.sampling_frequency = sampling_frequency
    # self.samples_number = samples_number

    #  def generate_time_axis(self):
    #     t = np.arange(0, (self.samples_number - 1) / self.sampling_frequency, self.time_step)
    #    ts = np.arange(0, (self.samples_number - 1) / self.sampling_frequency, 1 / self.sampling_frequency)
    #   return t, ts

    def generate_sine_wave(self, t, ts):
        signal_sampled = self.amplitude * np.sin(2 * np.pi * self.frequency * ts + np.deg2rad(self.phase))
        signal = self.amplitude * np.sin(2 * np.pi * self.frequency * t + np.deg2rad(self.phase))
        return signal_sampled, signal

    def __add__(self, other):
        self.amplitude * np.sin(
            2 * np.pi * self.frequency * self.t + np.deg2rad(self.phase)) + other.amplitude * np.sin(
            2 * np.pi * other.frequency * self.t + np.deg2rad(other.phase))


# def generate_fft(self):
#    sampled_signal = self.generate_sine_wave()[1]
#   f_x_axis = fftfreq(len(sampled_signal), 1 / self.sampling_frequency)
#  fft_signal = fft(sampled_signal)
# return f_x_axis, fft_signal

# def generate_ifft(self):
#    fft_data = self.generate_fft()[1]
#   ifft_data = ifft(fft_data)
#   return np.real(ifft_data)

#  def generate_dct(self):
#     sampled_signal = self.generate_sine_wave()[1]
#    return dct(sampled_signal, norm='ortho')

#  def generate_idct(self):
#     dct_data = self.generate_dct()
#    return idct(dct_data, norm='ortho')


# klasa odpowiadająca za kontrolę GUI(np. wcisniecie przycisku)
class Controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.update_button.clicked.connect(self.handle_update_button)
        self.view.add_button.clicked.connect(self.handle_add_button)

    def collect_data(self):
        amplitude_text = self.view.amplitude_edit.text()
        frequency_text = self.view.frequency_edit.text()
        phase_text = self.view.phase_edit.text()
        time_step_text = self.view.time_step_edit.text()
        sampling_frequency_text = self.view.sampling_fr_edit.text()
        signal_duration_text = self.view.signal_duration_edit.text()
        samples_number_text = self.view.samples_number_edit.text()

        if not (amplitude_text and frequency_text and signal_duration_text and
                sampling_frequency_text and phase_text and samples_number_text):
            print_error("Wprowadź wszystkie dane")
            return None

        amplitude = float(amplitude_text)
        frequency = float(frequency_text)
        phase = float(phase_text)
        time_step = float(time_step_text)
        sampling_frequency = float(sampling_frequency_text)
        signal_duration = float(signal_duration_text)
        samples_number = float(samples_number_text)

        data = {
            'amplitude': amplitude,
            'frequency': frequency,
            'phase': phase,
            'time_step': time_step,
            'sampling_frequency': sampling_frequency,
            'signal_duration': signal_duration,
            'samples_number': samples_number
        }
        return data

    def handle_add_button(self):
        data = self.collect_data()
        amplitude = data['amplitude']
        frequency = data['frequency']
        phase = data['phase']
        self.model.add_signal()

    def handle_update_button(self):
        self.view.clear_canvas()
        self.view.update_canvas('signal', t, signal, 'Original signal plot', 'plot', 'Time', 'Amplitude')
        self.view.update_canvas('signal', ts, signal_sampled, 'Original signal plot', 'stem', 'Time', 'Amplitude')
    #   fft_x, fft_signal = self.model.get_fft_data()
    #  self.view.update_canvas('dft', fft_x, np.abs(fft_signal), 'DFT plot', 'stem', 'Frequency', 'Magnitude')
    # reconstructed_signal = self.model.get_ifft_data()
    # self.view.update_canvas('ifft', ts, reconstructed_signal, 'IDFT plot', 'stem', 'Time', 'Amplitude')
    # dct_data = self.model.get_dct_data()
    # self.view.update_canvas('dct', fft_x, np.abs(dct_data), 'DCT plot', 'stem', 'Frequency', 'Magnitude')
    # idct_data = self.model.get_idct_data()
    # self.view.update_canvas('idct', ts, idct_data, 'IDCT plot', 'stem', 'Time', 'Amplitude')


# klasa odpowiadająca za stworzenie wykresu
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_model = MainModel()
    main_view = MainView()
    controller = Controller(main_view, main_model)
    main_view.show()
    sys.exit(app.exec_())
