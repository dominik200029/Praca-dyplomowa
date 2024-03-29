from scipy.fft import fftfreq
import numpy as np
from abc import ABC, abstractmethod


class Axis(ABC):
    """
    Abstract base class for representing an axis.

    Attributes:
        samples_number (int): The number of samples.
        sampling_frequency (float): The sampling frequency.

    Methods:
        generate(): Abstract method to generate the axis values.
    """
    def __init__(self, samples_number, sampling_frequency):
        """
        Initializes an Axis instance with a specified number of samples and sampling frequency.

        Parameters:
            samples_number (int): The number of samples.
            sampling_frequency (float): The sampling frequency.
        """
        self.samples_number = samples_number
        self.sampling_frequency = sampling_frequency

    @abstractmethod
    def generate(self):
        """
        Abstract method to generate the axis values.
        """
        pass


class TimeAxis(Axis):
    """
    Represents a time axis.

    Attributes:
        samples_number (int): The number of samples.
        sampling_frequency (float): The sampling frequency.
        time_step (float): The time step between samples.

    Methods:
        generate(): Generate the time axis values.
    """
    def __init__(self, samples_number, sampling_frequency, time_step):
        """
        Initializes a TimeAxis instance with specified number of samples, sampling frequency, and time step.

        Parameters:
            samples_number (int): The number of samples.
            sampling_frequency (float): The sampling frequency.
            time_step (float): The time step between samples.
        """
        super().__init__(samples_number, sampling_frequency)
        self.time_step = time_step

    def generate(self):
        """
        Generate the time axis values.

        Returns:
            numpy.ndarray: The time axis values.
        """
        return np.arange(0, self.samples_number / self.sampling_frequency, self.time_step)


class DiscreteTimeAxis(Axis):
    """
    Represents a discrete time axis.

    Attributes:
        samples_number (int): The number of samples.
        sampling_frequency (float): The sampling frequency.

    Methods:
        generate(): Generate the discrete time axis values.
    """
    def __init__(self, samples_number, sampling_frequency):
        """
        Initializes a DiscreteTimeAxis instance with specified number of samples and sampling frequency.

        Parameters:
            samples_number (int): The number of samples.
            sampling_frequency (float): The sampling frequency.
        """
        super().__init__(samples_number, sampling_frequency)

    def generate(self):
        """
        Generate the discrete time axis values.

        Returns:
            numpy.ndarray: The discrete time axis values.
        """
        return np.linspace(0, self.samples_number / self.sampling_frequency, self.samples_number)


class FrequencyAxis(Axis):
    """
    Represents a frequency axis.

    Attributes:
        samples_number (int): The number of samples.
        sampling_frequency (float): The sampling frequency.

    Methods:
        generate(): Generate the frequency axis values.
    """
    def __init__(self, samples_number, sampling_frequency):
        """
        Initializes a FrequencyAxis instance with specified number of samples and sampling frequency.

        Parameters:
            samples_number (int): The number of samples.
            sampling_frequency (float): The sampling frequency.
        """
        super().__init__(samples_number, sampling_frequency)

    def generate(self):
        """
        Generate the frequency axis values using FFT.

        Returns:
            numpy.ndarray: The frequency axis values.
        """
        return fftfreq(self.samples_number, d=1 / self.sampling_frequency)

