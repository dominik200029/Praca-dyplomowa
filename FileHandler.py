import cv2
from scipy.io import wavfile
from abc import ABC, abstractmethod


class FileHandler(ABC):
    """
    Abstract base class for handling files.

    Attributes:
        file_path (str): The path to the file.

    Methods:
        generate_data(): Abstract method to generate data from the file.
    """

    def __init__(self, file_path):
        """
        Initializes a FileHandler instance with the specified file path.

        Parameters:
            file_path (str): The path to the file.
        """
        self.file_path = file_path

    @abstractmethod
    def generate_data(self):
        """
        Abstract method to generate data from the file.
        """
        pass


class WavFileHandler(FileHandler):
    """
    Handles WAV files.

    Attributes:
        file_path (str): The path to the WAV file.

    Methods:
        generate_data(): Read the WAV file and return time axis, audio data, and sampling rate.
    """

    def __init__(self, file_path):
        """
        Initializes a WavFileHandler instance with the specified WAV file path.

        Parameters:
            file_path (str): The path to the WAV file.
        """
        super().__init__(file_path)

    def generate_data(self):
        """
        Read the WAV file and return time axis, audio data, and sampling rate.

        Returns:
            tuple: A tuple containing audio data, time axis, and sampling rate.
        """
        sampling_rate, data = wavfile.read(self.file_path)
        return data, sampling_rate


class JpgFileHandler(FileHandler):
    """
    Handles JPG image files.

    Attributes:
        file_path (str): The path to the JPG image file.

    Methods:
        generate_data(): Read the JPG image file and return the image data.
        plot_image(): Plot and display the JPG image using Matplotlib.
    """

    def __init__(self, file_path):
        """
        Initializes a JpgFileHandler instance with the specified JPG image file path.

        Parameters:
            file_path (str): The path to the JPG image file.
        """
        super().__init__(file_path)

    def generate_data(self):
        """
        Read the JPG image file and return the image data.

        Returns:
            numpy.ndarray: The image data as a NumPy array.
        """
        image = cv2.imread(self.file_path, 0)
        image_resized = cv2.resize(image, (64, 64))

        return image_resized
