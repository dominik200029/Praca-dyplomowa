import numpy as np
from PyQt5.QtWidgets import QFileDialog

from Controllers import Window
from Graph import Plot, StemPlot
from Signal import Sine
from Axis import TimeAxis, DiscreteTimeAxis, FFTAxis, DCTAxis
from TransformAnalyzer import FFTAnalyzer, IFFTAnalyzer, DCTAnalyzer, IDCTAnalyzer
from Filters import LowPassFilter, HighPassFilter, BandPassFilter, BandStopFilter


class Receiver:
    """
    Class for receiving and processing signals.

    Attributes:
        time_step (float): The time step.
        sampling_frequency (int): The sampling frequency.
        samples_number (int): The number of samples.
        time_axis (numpy.ndarray): The time axis.
        discrete_time_axis (numpy.ndarray): The discrete time axis.
        dft_frequencies (numpy.ndarray): The frequencies for the discrete Fourier transform.
        dct_frequencies (numpy.ndarray): The frequencies for the discrete cosine transform.
        wave (numpy.ndarray): The generated wave data.
        wave_from_file (numpy.ndarray): The wave data from a file.
        sampled_wave (numpy.ndarray): The sampled wave data.
        dft_data (numpy.ndarray): Result of the discrete Fourier transform.
        idft_data (numpy.ndarray): Result of the inverse discrete Fourier transform.
        dct_data (numpy.ndarray): Result of the discrete cosine transform.
        idct_data (numpy.ndarray): Result of the inverse discrete cosine transform.
        filtered_dft (numpy.ndarray): Filtered result of the discrete Fourier transform.
        filtered_idft (numpy.ndarray): Filtered result of the inverse discrete Fourier transform.
        filtered_dct (numpy.ndarray): Filtered result of the discrete cosine transform.
        filtered_idct (numpy.ndarray): Filtered result of the inverse discrete cosine transform.
        is_signal_from_file (bool): Indicates whether the signal is from a file.
        wav_filepath (str): The path to the WAV file.

    Methods:
        collect_data(controller): Collects data from the controller.
        collect_data_from_file(signals_handler): Collects data from a WAV file.
        add_signal_to_list(signals_handler, controller): Adds a sine signal to the list of signals.
        calculate_time_axis(): Calculates the time axis.
        calculate_discrete_time_axis(): Calculates the discrete time axis.
        calculate_dft_axis(): Calculates the frequencies for the discrete Fourier transform.
        calculate_dct_axis(): Calculates the frequencies for the discrete cosine transform.
        calculate_wave(signals_handler): Calculate the wave data.
        perform_dft(): Performs the discrete Fourier transform.
        perform_idft(): Performs the inverse discrete Fourier transform.
        perform_dct(): Performs the discrete cosine transform.
        perform_idct(): Performs the inverse discrete cosine transform.
        update_signal_plot(canvas): Updates the plot of the original signal.
        update_dft_plot(canvas): Updates the plot of the discrete Fourier transform.
        update_idft_plot(canvas): Updates the plot of the inverse discrete Fourier transform.
        update_dct_plot(canvas): Updates the plot of the discrete cosine transform.
        update_idct_plot(canvas): Updates the plot of the inverse discrete cosine transform.
        filter_dft(controller): Filters the discrete Fourier transform.
        filter_idft(): Filters the inverse discrete Fourier transform.
        filter_dct(controller): Filters the discrete cosine transform.
        filter_idct(): Filters the inverse discrete cosine transform.
        filtered_dft_plot(canvas): Plots the filtered discrete Fourier transform.
        filtered_idft_plot(canvas): Plots the filtered inverse discrete Fourier transform.
        filtered_dct_plot(canvas): Plots the filtered discrete cosine transform.
        filtered_idct_plot(canvas): Plots the filtered inverse discrete cosine transform.
        delete_signal(signals_handler, controller): Delete a signal from the list.
        update_signal(signals_handler, controller): Updates a signal in the list.
        handle_list_of_filters(controller): Handles the list of filters.
        choose_wav_file(controller): Opens a file dialog to choose a WAV file.
        show_window(controller): Shows the window.
        set_main_window_inactive(condition, controller): Sets the main window inactive.
    """

    def __init__(self):
        """
        Initializes a Receiver instance.
        """
        self.time_step = None
        self.sampling_frequency = None
        self.samples_number = None

        self.time_axis = None
        self.discrete_time_axis = None
        self.dft_frequencies = None
        self.dct_frequencies = None

        self.wave = None
        self.wave_from_file = None
        self.sampled_wave = None

        self.dft_data = None
        self.idft_data = None
        self.dct_data = None
        self.idct_data = None

        self.filtered_dft = None
        self.filtered_idft = None
        self.filtered_dct = None
        self.filtered_idct = None

        self.is_signal_from_file = False
        self.wav_filepath = None

    def collect_data(self, controller):
        """
        Collects data from the controller.

        Parameters:
            controller: The controller object.
        """
        self.sampling_frequency = controller.get_sampling_frequency()
        self.samples_number = controller.get_samples_number()
        self.time_step = controller.get_time_step()

    def collect_data_from_file(self, signals_handler):
        """
        Collects data from a WAV file.

        Parameters:
            signals_handler: The signal handler object.
        """
        if self.wav_filepath:
            self.wave, self.sampling_frequency = signals_handler.generate_from_file(self.wav_filepath)
            self.samples_number = len(self.wave)

    @staticmethod
    def add_signal_to_list(signals_handler, controller):
        """
        Adds a sine signal to the list of signals.

        Parameters:
            signals_handler: The signal handler object.
            controller: The controller object.
        """
        amplitude = controller.get_amplitude()
        frequency = controller.get_frequency()
        phase = controller.get_phase()

        signal = Sine(amplitude, frequency, phase)
        signals_handler.append_signal(signal)

    def calculate_time_axis(self):
        """Calculates the time axis."""
        self.time_axis = TimeAxis(self.samples_number, self.sampling_frequency, self.time_step).generate()

    def calculate_discrete_time_axis(self):
        """Calculates the discrete time axis."""
        self.discrete_time_axis = DiscreteTimeAxis(self.samples_number, self.sampling_frequency).generate()

    def calculate_dft_axis(self):
        """Calculates the frequencies for the discrete Fourier transform."""
        if self.samples_number and self.sampling_frequency:
            self.dft_frequencies = FFTAxis(self.samples_number, self.sampling_frequency).generate()

    def calculate_dct_axis(self):
        """Calculates the frequencies for the discrete cosine transform."""
        if self.samples_number and self.sampling_frequency:
            self.dct_frequencies = DCTAxis(self.samples_number, self.sampling_frequency).generate()

    def calculate_wave(self, signals_handler):
        """
        Calculates the wave data.

        Parameters:
            signals_handler: The signal handler object.
        """
        self.wave = signals_handler.generate_wave(self.time_axis)
        self.sampled_wave = signals_handler.generate_wave(self.discrete_time_axis)

    def perform_dft(self):
        """Performs the discrete Fourier transform."""
        if self.is_signal_from_file and self.wave is not None and self.wav_filepath is not None:
            self.dft_data = FFTAnalyzer(self.wave).calculate()
        elif self.sampled_wave is not None:
            self.dft_data = FFTAnalyzer(self.sampled_wave).calculate()

    def perform_idft(self):
        """Performs the inverse discrete Fourier transform."""
        if self.dft_data is not None:
            self.idft_data = IFFTAnalyzer(self.dft_data).calculate()

    def perform_dct(self):
        """Performs the discrete cosine transform."""
        if self.is_signal_from_file and self.wave is not None and self.wav_filepath is not None:
            self.dct_data = DCTAnalyzer(self.wave).calculate()
        elif self.sampled_wave is not None:
            self.dct_data = DCTAnalyzer(self.sampled_wave).calculate()

    def perform_idct(self):
        """Performs the inverse discrete cosine transform."""
        if self.dct_data is not None:
            self.idct_data = IDCTAnalyzer(self.dct_data).calculate()

    def update_signal_plot(self, canvas):
        """
        Updates the plot of the original signal.

        Parameters:
            canvas: The canvas to draw on.
        """
        signal_plot, sampled_signal_plot = None, None
        if self.is_signal_from_file:
            if self.wav_filepath is None:
                Window.plot_warning(canvas)
                return
            signal_plot = Plot(None, self.wave, 'Czas[s]', 'Amplituda', 'Sygnał oryginalny')
            if self.wave is None or (self.wave == 0).all():
                Window.plot_warning(canvas)
                return
        else:
            signal_plot = Plot(self.time_axis, self.wave, 'Czas[s]', 'Amplituda', 'Sygnał oryginalny')
            sampled_signal_plot = StemPlot(self.discrete_time_axis, self.sampled_wave, 'Czas[s]', 'Amplituda',
                                           'Sygnał oryginalny')
            if (self.wave == 0).all():
                Window.plot_warning(canvas)
                return
        canvas.clear()
        if signal_plot:
            signal_plot.create_on_canvas(canvas)
        if sampled_signal_plot:
            sampled_signal_plot.create_on_canvas(canvas)

    def update_dft_plot(self, canvas):
        """
        Updates the plot of the discrete Fourier transform.

        Parameters:
            canvas: The canvas to draw on.
        """
        if self.dft_data is not None:
            if (self.dft_data == 0).all():
                Window.plot_warning(canvas)
                return
            if self.is_signal_from_file:
                if self.wav_filepath is None:
                    Window.plot_warning(canvas)
                    return
                self.dft_frequencies = FFTAxis(self.samples_number, self.sampling_frequency).generate()
                dft_plot = Plot(self.dft_frequencies, np.abs(self.dft_data), 'Częstotliwość[Hz]', 'Amplituda',
                                'Moduł DFT')
            else:
                dft_plot = StemPlot(self.dft_frequencies, np.abs(self.dft_data), 'Częstotliwość[Hz]', 'Amplituda',
                                    'Moduł DFT')

            canvas.clear()
            dft_plot.create_on_canvas(canvas)

    def update_idft_plot(self, canvas):
        """
        Updates the plot of the inverse discrete Fourier transform.

        Parameters:
            canvas: The canvas to draw on.
        """
        if self.idft_data is not None:
            if (self.idft_data == 0).all():
                Window.plot_warning(canvas)
                return
            if self.is_signal_from_file:
                if self.wav_filepath is None:
                    Window.plot_warning(canvas)
                    return
                idft_plot = Plot(None, np.real(self.idft_data), 'Czas[s]', 'Amplituda', 'IDFT')
            else:
                idft_plot = StemPlot(self.discrete_time_axis, np.real(self.idft_data), 'Czas[s]', 'Amplituda', 'IDFT')

            canvas.clear()
            idft_plot.create_on_canvas(canvas)

    def update_dct_plot(self, canvas):
        """
        Updates the plot of the discrete cosine transform.

        Parameters:
            canvas: The canvas to draw on.
        """
        if self.dct_data is not None:
            if (self.dct_data == 0).all():
                Window.plot_warning(canvas)
                return
            if self.is_signal_from_file:
                if self.wav_filepath is None:
                    Window.plot_warning(canvas)
                    return
                self.dct_frequencies = DCTAxis(self.samples_number, self.sampling_frequency).generate()
                dct_plot = Plot(self.dct_frequencies, np.abs(self.dct_data), 'Częstotliwość[Hz]', 'Amplituda',
                                'Moduł DCT')
            else:
                dct_plot = StemPlot(self.dct_frequencies, np.abs(self.dct_data), 'Częstotliwość[Hz]', 'Amplituda',
                                    'Moduł DCT')

            canvas.clear()
            dct_plot.create_on_canvas(canvas)

    def update_idct_plot(self, canvas):
        """
        Updates the plot of the inverse discrete cosine transform.

        Parameters:
            canvas: The canvas to draw on.
        """
        if self.idct_data is not None:
            if (self.idct_data == 0).all():
                Window.plot_warning(canvas)
                return
            if self.is_signal_from_file:
                if self.wav_filepath is None:
                    Window.plot_warning(canvas)
                    return
                idct_plot = Plot(None, np.real(self.idct_data), 'Czas[s]', 'Amplituda', 'IDCT')
            else:
                idct_plot = StemPlot(self.discrete_time_axis, np.real(self.idct_data), 'Czas[s]', 'Amplituda', 'IDCT')

            canvas.clear()
            idct_plot.create_on_canvas(canvas)

    def filter_dft(self, controller):
        """
        Apply filtering to the discrete Fourier transform data.

        Parameters:
            controller: The controller object to retrieve filter parameters from.
        """
        filter_type = controller.filters_list.currentIndex()
        self.filtered_dft = np.copy(self.dft_data)
        indices_to_zero = []
        if filter_type == 1 or filter_type == 2:
            cut_off_frequency = controller.get_cut_off_frequency()
            if cut_off_frequency is not None:
                if filter_type == 1:  # Low-pass filter
                    indices_to_zero = LowPassFilter(cut_off_frequency).apply(self.dft_frequencies)
                elif filter_type == 2:  # High-pass filter
                    indices_to_zero = HighPassFilter(cut_off_frequency).apply(self.dft_frequencies)
        elif filter_type == 3 or filter_type == 4:
            low_cut_off_frequency = controller.get_low_cut_off_frequency()
            high_cut_off_frequency = controller.get_high_cut_off_frequency()
            if low_cut_off_frequency is not None and high_cut_off_frequency is not None:
                if low_cut_off_frequency >= high_cut_off_frequency:
                    controller.print_error('Dolna częstotliwość nie może być większa niż górna.')
                    return
                if filter_type == 3:  # Band-pass filter
                    indices_to_zero =\
                        BandPassFilter(low_cut_off_frequency, high_cut_off_frequency).apply(self.dft_frequencies)
                elif filter_type == 4:  # Band-stop filter
                    indices_to_zero =\
                        BandStopFilter(low_cut_off_frequency, high_cut_off_frequency).apply(self.dft_frequencies)
        else:
            controller.print_error('Wybierz filtr')
            return

        self.filtered_dft[indices_to_zero] = 0

    def filter_idft(self):
        """Apply filtering to the inverse discrete Fourier transform data."""
        self.filtered_idft = IFFTAnalyzer(self.filtered_dft).calculate()

    def filter_dct(self, controller):
        """
        Apply filtering to the discrete cosine transform data.

        Parameters:
            controller: The controller object to retrieve filter parameters from.
        """
        filter_type = controller.filters_list.currentIndex()
        self.filtered_dct = np.copy(self.dct_data)
        indices_to_zero = []
        if filter_type == 1 or filter_type == 2:
            cut_off_frequency = controller.get_cut_off_frequency()
            if cut_off_frequency is not None:
                if filter_type == 1: # Low-pass filter
                    indices_to_zero = LowPassFilter(cut_off_frequency).apply(self.dct_frequencies)
                elif filter_type == 2:  # High-pass filter
                    indices_to_zero = HighPassFilter(cut_off_frequency).apply(self.dct_frequencies)
        elif filter_type == 3 or filter_type == 4:
            low_cut_off_frequency = controller.get_low_cut_off_frequency()
            high_cut_off_frequency = controller.get_high_cut_off_frequency()
            if low_cut_off_frequency is not None and high_cut_off_frequency is not None:
                if low_cut_off_frequency >= high_cut_off_frequency:
                    controller.print_error('Dolna częstotliwość nie może być większa niż górna.')
                    return
                if filter_type == 3:  # Band-pass filter
                    indices_to_zero =\
                        BandPassFilter(low_cut_off_frequency, high_cut_off_frequency).apply(self.dct_frequencies)
                elif filter_type == 4:  # Band-stop filter
                    indices_to_zero =\
                        BandStopFilter(low_cut_off_frequency, high_cut_off_frequency).apply(self.dct_frequencies)
        else:
            controller.print_error('Wybierz filtr')
            return

        self.filtered_dct[indices_to_zero] = 0

    def filter_idct(self):
        """Apply filtering to the inverse discrete cosine transform data."""
        self.filtered_idct = IDCTAnalyzer(self.filtered_dct).calculate()

    def filtered_dft_plot(self, canvas):
        """
        Update the plot of the filtered discrete Fourier transform.

        Parameters:
            canvas: The canvas to draw on.
        """
        if self.is_signal_from_file:
            dft_plot = Plot(self.dft_frequencies, np.abs(self.filtered_dft), 'Częstotliwość[Hz]', 'Amplituda',
                            'Moduł DFT')
        else:
            dft_plot = StemPlot(self.dft_frequencies, np.abs(self.filtered_dft), 'Częstotliwość[Hz]', 'Amplituda',
                                'Moduł DFT')
        canvas.clear()
        dft_plot.create_on_canvas(canvas)

    def filtered_idft_plot(self, canvas):
        """
        Update the plot of the filtered inverse discrete Fourier transform.

        Parameters:
            canvas: The canvas to draw on.
        """
        if self.is_signal_from_file:
            idft_plot = Plot(None, np.real(self.filtered_dft), 'Czas[s]', 'Amplituda', 'IDFT')
        else:
            idft_plot = StemPlot(self.discrete_time_axis, np.real(self.filtered_idft), 'Czas[s]', 'Amplituda',
                                 'IDFT')
        canvas.clear()
        idft_plot.create_on_canvas(canvas)

    def filtered_dct_plot(self, canvas):
        """
        Update the plot of the filtered discrete cosine transform.

        Parameters:
            canvas: The canvas to draw on.
        """
        if self.is_signal_from_file:
            dct_plot = Plot(self.dct_frequencies, np.abs(self.filtered_dct), 'Częstotliwość[Hz]', 'Amplituda',
                            'Moduł DCT')
        else:
            dct_plot = StemPlot(self.dct_frequencies, np.abs(self.filtered_dct), 'Częstotliwość[Hz]', 'Amplituda',
                                'Moduł DCT')
        canvas.clear()
        dct_plot.create_on_canvas(canvas)

    def filtered_idct_plot(self, canvas):
        """
        Update the plot of the filtered inverse discrete cosine transform.

        Parameters:
            canvas: The canvas to draw on.
        """
        if self.is_signal_from_file:
            idct_plot = Plot(None, np.real(self.filtered_idct), 'Czas[s]', 'Amplituda', 'IDCT')
        else:
            idct_plot = StemPlot(self.discrete_time_axis, np.real(self.filtered_idct), 'Czas[s]', 'Amplituda', 'IDCT')
        canvas.clear()
        idct_plot.create_on_canvas(canvas)

    @staticmethod
    def delete_signal(signals_handler, controller):
        """
        Delete a signal from the list of signals.

        Parameters:
            signals_handler: The signals handler object containing the list of signals.
            controller: The controller object to retrieve the signal number from.
        """
        signal_number = controller.get_signal_number()
        if signal_number:
            index = signal_number - 1
            signal_amount = signals_handler.signal_amount

            list_of_signals = signals_handler.signals
            list_of_signals_labels = signals_handler.signals_labels

            if list_of_signals and list_of_signals_labels and 0 <= index < signal_amount:
                list_of_signals.pop(index)
                list_of_signals_labels.pop(index)
                signals_handler.signal_amount -= 1
        else:
            controller.print_error('Aby usunać daną składową, musisz zaznaczyć pole.')

    @staticmethod
    def update_signal(signals_handler, controller):
        """
        Update a signal in the list of signals.

        Parameters:
            signals_handler: The signals handler object containing the list of signals.
            controller: The controller object to retrieve the signal parameters from.
        """
        signal_number = controller.get_signal_number()
        if signal_number:
            index = signal_number - 1
            if index < signals_handler.signal_amount:
                signal = signals_handler.signals[index]
            else:
                return

            amplitude = controller.get_amplitude()
            frequency = controller.get_frequency()
            phase = controller.get_phase()

            signal.amplitude = amplitude
            signal.frequency = frequency
            signal.phase = phase

            signals_handler.signals_labels[index] = signal.signal_to_text()

    @staticmethod
    def handle_list_of_filters(controller):
        """
        Handle the list of available filters.

        Parameters:
            controller: The controller object to retrieve filter parameters from.
        """
        filter_type = controller.get_filters_list_index()
        if filter_type == 0:
            controller.set_spinBoxes_access(True, True, True)
        elif filter_type == 1:
            controller.set_spinBoxes_access(True, True, False)
        elif filter_type == 2:
            controller.set_spinBoxes_access(True, True, False)
        elif filter_type == 3:
            controller.set_spinBoxes_access(False, False, True)
        elif filter_type == 4:
            controller.set_spinBoxes_access(False, False, True)

    def choose_wav_file(self, controller):
        """
        Choose a WAV file.

        Parameters:
            controller: The controller object to update the file name display.
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, 'Choose Audio File', filter='WAV files (*.wav);')
        controller.file_name.setPlainText(str(file_path))
        self.wav_filepath = str(file_path)

    @staticmethod
    def show_window(controller):
        """
        Show the main window.

        Parameters:
            controller: The controller object representing the main window.
        """
        controller.show()

    def set_main_window_inactive(self, condition: bool, controller):
        """
        Set the main window to be inactive based on a condition.

        Parameters:
            condition: The condition to determine whether the main window should be inactive.
            controller: The controller object representing the main window.
        """
        if condition:
            self.is_signal_from_file = True
            controller.amplitude_spinBox.setDisabled(True)
            controller.frequency_spinBox.setDisabled(True)
            controller.phase_spinBox.setDisabled(True)
            controller.sampling_frequency_spinBox.setDisabled(True)
            controller.samples_number_spinBox.setDisabled(True)
            controller.time_step_spinBox.setDisabled(True)
            controller.signal_number_spinBox.setDisabled(True)
            controller.add_button.setDisabled(True)
            controller.delete_signal_button.setDisabled(True)
            controller.signal_number_checkBox.setDisabled(True)

        else:
            self.is_signal_from_file = False
            self.wave_from_file = None
            controller.amplitude_spinBox.setDisabled(False)
            controller.frequency_spinBox.setDisabled(False)
            controller.phase_spinBox.setDisabled(False)
            controller.sampling_frequency_spinBox.setDisabled(False)
            controller.samples_number_spinBox.setDisabled(False)
            controller.time_step_spinBox.setDisabled(False)
            controller.signal_number_spinBox.setDisabled(False)
            controller.add_button.setDisabled(False)
            controller.delete_signal_button.setDisabled(False)
            controller.signal_number_checkBox.setDisabled(False)
