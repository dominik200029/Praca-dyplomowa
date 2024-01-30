import numpy as np
from FileHandler import WavFileHandler, JpgFileHandler
from abc import ABC, abstractmethod


class SignalsHandler(ABC):
    """
        Abstract base class for handling signals.

        """
    def __init__(self):
        self.signals = []
        self.signals_labels = []
        self.signal_amount = 0

    @abstractmethod
    def append_signal(self, signal):
        pass

    @abstractmethod
    def generate_wave(self, x_axis):
        pass

    @staticmethod
    @abstractmethod
    def generate_from_file(file):
        pass


class SineHandler(SignalsHandler):
    """
    Class for handling signals.

    Attributes:
        signals (list): List to store Signal instances.
        signals_labels (list): List to store labels of Signal instances.
        signal_amount (int): The total number of signals.

    Methods:
        append_signal(signal): Append a Signal instance to the list of signals.
        generate_wave(x_axis): Generate the composite wave from the stored signals.
        generate_wave_from_file(file): Generate wave data from a WAV file using WavFileHandler.
    """

    def __init__(self):
        """
        Initializes a SignalsHandler instance.
        """
        super().__init__()

    def append_signal(self, signal):
        """
        Append a signal to the list of signals.

        Parameters:
            signal : The instance to be appended.
        """
        self.signals.append(signal)
        self.signals_labels.append(signal.signal_to_text())
        self.signal_amount += 1

    def generate_wave(self, x_axis):
        """
        Generate the composite wave from the stored signals.

        Parameters:
            x_axis (numpy.ndarray): Time axis values for the continuous wave.

        Returns:
            tuple: A tuple containing the continuous wave and sampled wave.
        """
        wave = np.zeros(len(x_axis))  # initialize wave vector with zeros

        for signal in self.signals:
            wave += signal.get_wave(x_axis)

        return wave

    @staticmethod
    def generate_from_file(file):
        """
        Generate wave data from a WAV file using WavFileHandler.

        Parameters:
            file (str): The path to the WAV file.

        Returns:
            tuple: A tuple containing audio data, time axis, and sampling frequency.
        """
        file_handler = WavFileHandler(file)
        data, sampling_frequency = file_handler.generate_data()
        return data, sampling_frequency

    def get_text(self):
        text = ''
        for label in self.signals_labels:
            text += label
        return text


class Sine2DHandler(SignalsHandler):
    def __init__(self):
        super().__init__()

    def append_signal(self, signal):
        pass

    def generate_wave(self, x_axis):
        pass

    @staticmethod
    def generate_from_file(file):
        return JpgFileHandler(file).generate_data()

