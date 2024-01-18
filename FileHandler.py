from scipy.io import wavfile
import numpy as np
from abc import ABC, abstractmethod


class FileHandler(ABC):
    """
    Abstract base class for handling files.

    Attributes:
        file (str): The path to the file.

    Methods:
        generate_data(): Abstract method to generate data from the file.
    """

    def __init__(self, file):
        """
        Initializes a FileHandler instance with the specified file path.

        Parameters:
            file (str): The path to the file.
        """
        self.file = file

    @abstractmethod
    def generate_data(self):
        """
        Abstract method to generate data from the file.
        """
        pass


class WavFileHandler(FileHandler):
    """
    Handles WAV files and generates time axis and audio data.

    Attributes:
        file (str): The path to the WAV file.

    Methods:
        generate_data(): Read the WAV file and return time axis, audio data, and sampling rate.
    """

    def __init__(self, file):
        """
        Initializes a WavFileHandler instance with the specified WAV file path.

        Parameters:
            file (str): The path to the WAV file.
        """
        super().__init__(file)

    def generate_data(self):
        """
        Read the WAV file and return time axis, audio data, and sampling rate.

        Returns:
            tuple: A tuple containing audio data, time axis, and sampling rate.
        """
        sampling_rate, data = wavfile.read(self.file)
        duration = len(data) / sampling_rate
        time_axis = np.linspace(0, duration, len(data))
        return data, time_axis, sampling_rate
