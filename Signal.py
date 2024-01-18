import numpy as np
from abc import ABC, abstractmethod


class Signal(ABC):
    """
    Abstract base class representing a signal.

    Attributes:
    - amplitude (float): The amplitude of the signal.
    """

    def __init__(self, amplitude):
        """
        Initializes a Signal object.

        Parameters:
        - amplitude (float): The amplitude of the signal.
        """
        self.amplitude = amplitude

    @abstractmethod
    def signal_to_text(self):
        """
        Abstract method to convert the signal information to text.

        Returns:
        - str: Text representation of the signal.
        """
        pass

    @abstractmethod
    def get_wave(self, x_axis):
        """
        Abstract method to generate the waveform of the signal.

        Parameters:
        - x_axis (numpy.ndarray): The time values for which the waveform should be generated.

        Returns:
        - numpy.ndarray: The waveform of the signal.
        """
        pass


class Sine(Signal):
    """
    A class representing a sine wave signal.

    Attributes:
    - frequency (float): The frequency of the sine wave.
    - phase (float): The phase of the sine wave in degrees.
    """

    def __init__(self, amplitude, frequency, phase):
        """
        Initializes a Sine object.

        Parameters:
        - amplitude (float): The amplitude of the sine wave.
        - frequency (float): The frequency of the sine wave.
        - phase (float): The phase of the sine wave in degrees.
        """
        super().__init__(amplitude)
        self.frequency = frequency
        self.phase = phase

    def signal_to_text(self):
        """
        Converts the sine wave signal information to text.

        Returns:
        - str: Text representation of the sine wave signal.
        """
        amplitude_text = str(self.amplitude)
        frequency_text = str(self.frequency)
        phase_text = str(self.phase)
        return f"{amplitude_text} sin(2π*{frequency_text}*t+{phase_text})\n"

    def get_wave(self, time):
        """
        Generates the waveform of the sine wave.

        Parameters:
        - time (numpy.ndarray): The time values for which the waveform should be generated.

        Returns:
        - numpy.ndarray: The waveform of the sine wave.
        """
        if self.amplitude and self.frequency and self.phase:
            return self.amplitude * np.sin(2 * np.pi * self.frequency * time + np.deg2rad(self.phase))
