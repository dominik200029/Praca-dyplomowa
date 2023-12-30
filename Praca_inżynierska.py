import os
import sys
import numpy as np

from scipy.fft import fft, ifft, dct, idct, fftfreq
from scipy.io import wavfile

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt5.uic import loadUi

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


# Canvas class handles plotting in the GUI
class Canvas:
    def __init__(self, layout):
        self.figure = Figure(figsize=(5, 5))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(NavigationToolbar(self.canvas, None))
        layout.addWidget(self.canvas)
        self.ax = self.figure.subplots()

    def plot(self, x, y, title, plot_type, x_label, y_label):
        # Plot the given data based on the specified plot type
        if plot_type == 'stem':
            self.ax.stem(x, y)
        elif plot_type == 'plot':
            self.ax.plot(x, y)
        else:
            raise Exception('Plot type can be either "plot" or "stem"')
        # Set labels and title, then draw the canvas
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(title)
        self.ax.figure.canvas.draw()

    def clear_canvas(self):
        # Clear the plot in the canvas
        self.ax.clear()

# WavFileHandler class handles reading audio data from a WAV file
class WavFileHandler:
    def __init__(self, file):
        self.file = file

    def get_audio_data(self):
        # Read the WAV file and return time axis and audio data
        sampling_rate, data = wavfile.read(self.file)
        duration = len(data) / sampling_rate
        time_axis = np.linspace(0., duration, len(data))
        return data, time_axis


# AxisHandler class manages generating different time and frequency axes
class AxisHandler:
    def __init__(self, data):
        self.samples_number = data['samples_number']
        self.sampling_frequency = data['sampling_frequency']
        self.time_step = data['time_step']

    def generate_time_axis(self):
        # Generate a time axis based on the given parameters
        time_axis = np.arange(0, self.samples_number / self.sampling_frequency, self.time_step)
        return time_axis

    def generate_discrete_time_axis(self):
        # Generate a discrete time axis
        discrete_time_axis = np.linspace(0, self.samples_number / self.sampling_frequency, self.samples_number,
                                         endpoint=False)
        return discrete_time_axis

    def generate_frequency_axis(self):
        # Generate a frequency axis using the FFT frequency function
        fft_x_axis = fftfreq(self.samples_number, d=1 / self.sampling_frequency)
        return fft_x_axis


# Signal class represents a sine wave signal
class Signal:
    def __init__(self, amplitude, frequency, phase):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase


# TransformAnalyzer class performs FFT, IFFT, DCT, and IDCT on signals
class TransformAnalyzer:
    def __init__(self, signal):
        self.signal = signal

    def calculate_fft(self, data):
        # Create an AxisHandler instance to generate frequency axis
        axis = AxisHandler(data)
        fft_x_axis = axis.generate_frequency_axis()
        # Perform FFT on the signal and return the result
        fft_data = fft(self.signal)
        return fft_x_axis, fft_data

    @staticmethod
    def calculate_ifft(fft_function):
        # Perform IFFT on the given FFT function and return the result
        ifft_data = ifft(fft_function)
        return ifft_data

    def calculate_dct(self, data):
        # Create an AxisHandler instance to generate frequency axis
        axis = AxisHandler(data)
        dct_x_axis = axis.generate_frequency_axis()
        # Perform DCT on the signal with normalization and return the result
        dct_data = dct(self.signal, norm='ortho')
        return dct_x_axis, dct_data

    @staticmethod
    def calculate_idct(dct_function):
        # Perform IDCT on the given DCT function with normalization and return the result
        idct_data = idct(dct_function, norm='ortho')
        return idct_data


# View class represents the main GUI window
class View(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi('gui.ui', self)

        # Dictionary to hold Canvas instances for different plots
        self.canvas_dict = {
            'signal': Canvas(self.layout1),
            'fft': Canvas(self.layout2),
            'ifft': Canvas(self.layout3),
            'dct': Canvas(self.layout4),
            'idct': Canvas(self.layout5)
        }

    def update_canvas(self, canvas_type, x, y, title, plot_type, x_label, y_label):
        # Update the specified canvas with the given data
        canvas = self.canvas_dict.get(canvas_type)
        if canvas:
            canvas.plot(x, y, title, plot_type, x_label, y_label)

    def clear_canvas(self):
        # Clear all plots in the canvas
        for canvas in self.canvas_dict.values():
            if canvas:
                canvas.clear_canvas()

    @staticmethod
    def print_error(message):
        # Display an error message in a pop-up dialog
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()


# Model class represents the data and logic of the application
class Model:
    def __init__(self):
        # Initialize signals count and list
        self.signals_amount = 0
        self.signals = []

    def add_signal(self, data):
        # Add a new signal to the list based on user input
        self.signals.append(Signal(data['amplitude'][self.signals_amount], data['frequency'][self.signals_amount],
                                   data['phase'][self.signals_amount]))
        self.signals_amount += 1

    def generate_wave(self, data):
        # Generate a composite wave based on the added signals
        axis = AxisHandler(data)
        time_axis = axis.generate_time_axis()
        discrete_time_axis = axis.generate_discrete_time_axis()
        wave = np.zeros(len(time_axis))
        sampled_wave = np.zeros(len(discrete_time_axis))

        for signal in self.signals:
            # Combine individual signals to form the composite wave
            wave += signal.amplitude * np.sin(2 * np.pi * signal.frequency * time_axis + np.deg2rad(signal.phase))
            sampled_wave += signal.amplitude * np.sin(2 * np.pi * signal.frequency * discrete_time_axis
                                                      + np.deg2rad(signal.phase))
        return time_axis, discrete_time_axis, wave, sampled_wave

    def generate_wave_from_file(self, file):
        # Read audio data from a WAV file and return sampling frequency and data
        file_handler = WavFileHandler(file)
        sampling_frequency, data = file_handler.get_audio_data()
        return sampling_frequency, data

    def generate_fft(self, axis_data, wave):
        # Calculate FFT of the sampled wave and return the result
        fft_analyzer = TransformAnalyzer(wave)
        fft_axis, fft_data = fft_analyzer.calculate_fft(axis_data)
        return fft_axis, fft_data

    @staticmethod
    def generate_ifft(fft_function):
        # Calculate IFFT of the given FFT function and return the result
        ifft_data = TransformAnalyzer.calculate_ifft(fft_function)
        return ifft_data

    def generate_dct(self, axis_data, wave):
        # Calculate DCT of the sampled wave and return the result
        dct_analyzer = TransformAnalyzer(wave)
        dct_x_axis, dct_data = dct_analyzer.calculate_dct(axis_data)
        return dct_x_axis, dct_data

    @staticmethod
    def generate_idct(dct_function):
        # Calculate IDCT of the given DCT function and return the result
        idct_data = TransformAnalyzer.calculate_idct(dct_function)
        return idct_data


# Controller class manages the interaction between the model and the view
class Controller:
    def __init__(self, model, view):
        # Initialize the model, view, and lists to store signal parameters
        self.model = model
        self.view = view
        self.amplitude = []
        self.frequency = []
        self.phase = []
        self.filename = ''

    def collect_signal_data(self):
        # Collect amplitude, frequency, and phase data from the user input
        amplitude_text = self.view.amplitude_edit.text()
        frequency_text = self.view.frequency_edit.text()
        phase_text = self.view.phase_edit.text()

        if not (amplitude_text and frequency_text and phase_text):
            View.print_error("Wprowadz wszystkie dane")
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
        # Collect time step, sampling frequency, and samples number data from the user input
        time_step_text = self.view.time_step_edit.text()
        sampling_frequency_text = self.view.sampling_frequency_edit.text()
        samples_number_text = self.view.samples_number_edit.text()

        if not (time_step_text and sampling_frequency_text and samples_number_text):
            View.print_error("Wprowadz wszystkie dane")
            return None

        # Check if data is greater than zero before converting to float
        try:
            time_step = float(time_step_text)
            sampling_frequency = float(sampling_frequency_text)
            samples_number = int(samples_number_text)

            # Check if all data is greater than zero
            if time_step > 0 and sampling_frequency > 0 and samples_number > 0:
                data = {
                    'time_step': time_step,
                    'sampling_frequency': sampling_frequency,
                    'samples_number': samples_number
                }
                return data
            else:
                View.print_error("Wszystkie dane muszą być większe niż zero")
                return None

        except ValueError:
            View.print_error("Nieprawidłowy format danych. Wprowadź liczby.")
            return None

    def handle_update_button(self):
        # Handle the update button click event
        self.view.clear_canvas()
        data = self.collect_axis_data()
        time_axis, discrete_time_axis, wave, sampled_wave = self.model.generate_wave(data)
        if self.view.wave_from_file.isChecked():
            wave, time_axis = self.model.generate_wave_from_file(self.filename)
        self.view.update_canvas('signal', time_axis, wave, 'Original signal', 'plot', 'Time',
                                'Amplitude')
        fft_x_data, fft_data = self.model.generate_fft(data, sampled_wave)
        self.view.update_canvas('fft', fft_x_data, abs(fft_data), 'abs(FFT)', 'stem', 'Frequency',
                                'Amplitude')
        ifft_data = self.model.generate_ifft(fft_data)
        self.view.update_canvas('ifft', discrete_time_axis, np.real(ifft_data), 'Inverse FFT', 'stem', 'Time',
                                'Amplitude')
        dct_axis_data, dct_data = self.model.generate_dct(data, sampled_wave)
        self.view.update_canvas('dct', dct_axis_data, dct_data, 'DCT', 'stem', 'Frequency', 'Magnitude')
        idct_data = self.model.generate_idct(dct_data)
        self.view.update_canvas('idct', discrete_time_axis, np.real(idct_data), 'IDCT', 'stem', 'Time', 'Amplitude')

    def handle_choose_file_button(self):
        # Handle the choose file button click event
        options = QFileDialog.Options()

        file_dialog = QFileDialog()
        file_dialog.setOptions(options)

        # Set file dialog properties, if needed
        file_dialog.setNameFilter("Wave files (*.wav);;All files (*)")
        file_dialog.setViewMode(QFileDialog.Detail)

        # Show the dialog and get the selected file(s)
        result = file_dialog.exec_()

        if result == QFileDialog.Accepted:
            selected_files = file_dialog.selectedFiles()

            # Process the selected file (only the first one)
            if selected_files:
                selected_file = selected_files[0]
                filename_with_extension = os.path.basename(selected_file)
                self.filename = filename_with_extension
                self.view.file_name.setPlainText(filename_with_extension)

    def handle_add_button(self):
        # Handle the add button click event
        data = self.collect_signal_data()
        signal_number = self.model.signals_amount
        self.model.add_signal(data)
        # Retrieve the existing text from the label
        existing_text = self.view.signal_label.toPlainText()
        # Add information about the new signal
        text = (f"{existing_text}\n{data['amplitude'][signal_number]}sin(2*π*t*{data['frequency'][signal_number]}"
                f"+{data['phase'][signal_number]}°)+")
        # Update the label with the new text
        self.view.signal_label.setPlainText(text)


# Application class representing the main application
class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        # Initialize the model, view, and controller
        self.model = Model()
        self.view = View()
        self.controller = Controller(self.model, self.view)

        # Connect UI signals to controller methods
        self.view.add_button.clicked.connect(self.controller.handle_add_button)
        self.view.sampling_frequency_edit.valueChanged.connect(self.controller.handle_update_button)
        self.view.samples_number_edit.valueChanged.connect(self.controller.handle_update_button)
        self.view.choose_file_button.clicked.connect(self.controller.handle_choose_file_button)
        self.view.update_button.clicked.connect(self.controller.handle_update_button)

        # Show the main window
        self.view.show()


# Main entry point
if __name__ == '__main__':
    # Create the application and start the event loop
    app = App(sys.argv)
    sys.exit(app.exec_())
