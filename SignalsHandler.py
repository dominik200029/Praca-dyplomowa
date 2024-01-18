import numpy as np
from FileHandler import WavFileHandler


class SignalsHandler:
    """
    Class for handling signals.

    Attributes:
        signals (list): List to store Signal instances.
        signals_labels (list): List to store labels of Signal instances.
        signal_amount (int): The total number of signals.

    Methods:
        append_signal(signal): Append a Signal instance to the list of signals.
        generate_wave(time_axis, discrete_time_axis): Generate the composite wave from the stored signals.
        generate_wave_from_file(file): Generate wave data from a WAV file using WavFileHandler.
    """

    def __init__(self):
        """
        Initializes a SignalsHandler instance.
        """
        self.signals = []
        self.signals_labels = []
        self.signal_amount = 0

    def append_signal(self, signal):
        """
        Append a signal to the list of signals.

        Parameters:
            signal : The instance to be appended.
        """
        self.signals.append(signal)
        self.signals_labels.append(signal.signal_to_text())
        self.signal_amount += 1

    def generate_wave(self, time_axis, discrete_time_axis):
        """
        Generate the composite wave from the stored signals.

        Parameters:
            time_axis (numpy.ndarray): Time axis values for the continuous wave.
            discrete_time_axis (numpy.ndarray): Time axis values for the sampled wave.

        Returns:
            tuple: A tuple containing the continuous wave and sampled wave.
        """
        wave = np.zeros(len(time_axis))  # initialize wave vector with zeros
        sampled_wave = np.zeros(len(discrete_time_axis))  # initialize sampled_wave vector with zeros

        for signal in self.signals:
            wave += signal.get_wave(time_axis)
            sampled_wave += signal.get_wave(discrete_time_axis)

        return wave, sampled_wave

    @staticmethod
    def generate_wave_from_file(file):
        """
        Generate wave data from a WAV file using WavFileHandler.

        Parameters:
            file (str): The path to the WAV file.

        Returns:
            tuple: A tuple containing audio data, time axis, and sampling frequency.
        """
        file_handler = WavFileHandler(file)
        data, time_axis, sampling_frequency = file_handler.generate_data()
        return data, time_axis, sampling_frequency

    def get_text(self):
        text = ''
        for label in self.signals_labels:
            text += label
        return text
