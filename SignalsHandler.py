import numpy as np
from FileHandler import WavFileHandler, JpgFileHandler
from abc import ABC, abstractmethod


class SignalsHandler(ABC):
    """
    Abstract base class for handling signals.

    Attributes:
        signals (list): List to store Signal instances.
        signals_labels (list): List to store labels of Signal instances.
        signal_amount (int): The total number of signals.

    Methods:
        append_signal(signal): Append a Signal instance to the list of signals.
        generate_wave(x_axis): Generate the composite wave from the stored signals.
        generate_wave_from_file(file): Generate wave data from a file.
    """

    def __init__(self):
        """
        Initializes a SignalsHandler instance.
        """
        self.signals = []
        self.signals_labels = []
        self.signal_amount = 0

    @abstractmethod
    def append_signal(self, signal):
        """
        Append a signal to the list of signals.

        Parameters:
            signal : The instance to be appended.
        """
        pass

    @abstractmethod
    def generate_wave(self, x_axis):
        """
        Generate the composite wave from the stored signals.

        Parameters:
            x_axis (numpy.ndarray): Time axis values for the continuous wave.

        Returns:
            tuple: A tuple containing the continuous wave and sampled wave.
        """
        pass

    @staticmethod
    @abstractmethod
    def generate_from_file(file):
        """
        Generate wave data from a file.

        Parameters:
            file (str): The path to the file.

        Returns:
            tuple: A tuple containing audio data, time axis, and sampling frequency.
        """
        pass


class SineHandler(SignalsHandler):
    """
    Class for handling sine wave signals.

    Attributes:
        signals (list): List to store Sine instances.
        signals_labels (list): List to store labels of Sine instances.
        signal_amount (int): The total number of sine signals.

    Methods:
        append_signal(signal): Append a Sine instance to the list of signals.
        generate_wave(x_axis): Generate the composite wave from the stored sine signals.
        generate_wave_from_file(file): Generate wave data from a WAV file using WavFileHandler.
        get_text(): Get text representation of the signals.
    """

    def __init__(self):
        """
        Initializes a SineHandler instance.
        """
        super().__init__()

    def append_signal(self, signal):
        """
        Append a sine signal to the list of signals.

        Parameters:
            signal : The sine signal instance to be appended.
        """
        self.signals.append(signal)
        self.signals_labels.append(signal.signal_to_text())
        self.signal_amount += 1

    def generate_wave(self, x_axis):
        """
        Generate the composite wave from the stored sine signals.

        Parameters:
            x_axis (numpy.ndarray): Time axis values for the continuous wave.

        Returns:
            numpy.ndarray: The composite wave generated from the stored sine signals.
        """
        wave = np.zeros(len(x_axis))

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
        """
        Get text representation of the signals.

        Returns:
            str: Text representation of the signals.
        """
        text = ''
        if self.signal_amount == 0:
            text = 'Wybierz parametry, a następnie dodaj sygnał'
        else:
            for label in self.signals_labels:
                text += label
        return text


class Sine2DHandler(SignalsHandler):
    """
    Class for handling two-dimensional sine signals.

    Attributes:
        signals (list): List to store Sine2D instances.
        signals_labels (list): List to store labels of Sine2D instances.
        signal_amount (int): The total number of two-dimensional sine signals.

    Methods:
        append_signal(signal): Append a Sine2D instance to the list of signals.
        generate_wave(size): Generate the composite wave from the stored two-dimensional sine signals.
        generate_wave_from_file(file): Generate wave data from a JPG file using JpgFileHandler.
    """

    def __init__(self):
        """
        Initializes a Sine2DHandler instance.
        """
        super().__init__()

    def append_signal(self, signal):
        """
        Append a two-dimensional sine signal to the list of signals.

        Parameters:
            signal : The two-dimensional sine signal instance to be appended.
        """
        self.signals.append(signal)

    def generate_wave(self, size):
        """
        Generate the composite wave from the stored two-dimensional sine signals.

        Parameters:
            size (int): Size of the two-dimensional wave.

        Returns:
            numpy.ndarray: The composite wave generated from the stored two-dimensional sine signals.
        """
        # Stub implementation, as generating 2D wave is not yet implemented
        return

    @staticmethod
    def generate_from_file(file):
        """
        Generate wave data from a JPG file using JpgFileHandler.

        Parameters:
            file (str): The path to the JPG file.

        Returns:
            numpy.ndarray: Image data from the JPG file.
        """
        return JpgFileHandler(file).generate_data()
