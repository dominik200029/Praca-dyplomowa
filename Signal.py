import numpy as np
from abc import ABC, abstractmethod


class Signal(ABC):
    """
    Abstract base class representing a signal.

    Attributes:
        amplitude (float): The amplitude of the signal.
    """

    def __init__(self, amplitude):
        """
        Initializes a Signal object.

        Parameters:
            amplitude (float): The amplitude of the signal.
        """
        self.amplitude = amplitude

    @abstractmethod
    def signal_to_text(self):
        """
        Abstract method to convert the signal information to text.

        Returns:
            str: Text representation of the signal.
        """
        pass

    @abstractmethod
    def get_wave(self, x_axis):
        """
        Abstract method to generate the waveform of the signal.

        Parameters:
            x_axis (numpy.ndarray): The time values for which the waveform should be generated.

        Returns:
            numpy.ndarray: The waveform of the signal.
        """
        pass


class Sine(Signal):
    """
    A class representing a sine wave signal.

    Attributes:
        frequency (float): The frequency of the sine wave.
        phase (float): The phase of the sine wave in degrees.
    """

    def __init__(self, amplitude, frequency, phase):
        """
        Initializes a Sine object.

        Parameters:
            amplitude (float): The amplitude of the sine wave.
            frequency (float): The frequency of the sine wave.
            phase (float): The phase of the sine wave in degrees.
        """
        super().__init__(amplitude)
        self.frequency = frequency
        self.phase = phase

    def signal_to_text(self):
        """
        Converts the sine wave signal information to text.

        Returns:
            str: Text representation of the sine wave signal.
        """
        amplitude_text = str(int(self.amplitude)) if self.amplitude.is_integer() else str(self.amplitude)
        frequency_text = str(int(self.frequency)) if self.frequency.is_integer() else str(self.frequency)

        if self.phase == 0:
            phase_text = ""
        elif self.phase > 0:
            phase_text = f"+{int(self.phase)}" if self.phase.is_integer() else f"+{self.phase}"
        else:
            phase_text = f"{int(self.phase)}" if self.phase.is_integer() else f"{self.phase}"

        return f"{amplitude_text} sin(2π*{frequency_text}*t{phase_text})\n"

    def get_wave(self, time):
        """
        Generates the waveform of the sine wave.

        Parameters:
            time (numpy.ndarray): The time values for which the waveform should be generated.

        Returns:
            numpy.ndarray: The waveform of the sine wave.
        """
        return self.amplitude * np.sin(2 * np.pi * self.frequency * time + np.deg2rad(self.phase))


class Sine2D(Signal):
    """
    A class representing a 2D sine wave signal.

    Attributes:
        spatial_frequency (float): The frequency of the sine wave along the x-axis.
        angle (float): The angle of rotation in degrees.
    """

    def __init__(self, spatial_frequency, angle, amplitude=0):
        """
        Initializes a Sine2D object.

        Parameters:
            spatial_frequency (float): The frequency of the sine wave along the x-axis.
            angle (float): The angle of rotation in degrees.
            amplitude (float, optional): The amplitude of the sine wave.
            Default to 0.
        """
        super().__init__(amplitude)
        self.spatial_frequency = spatial_frequency
        self.angle = angle

    def signal_to_text(self):
        """
        Converts the 2D sine wave signal information to text.

        Returns:
            str: Text representation of the 2D sine wave signal.
        """
        spatial_frequency_text = str(int(self.spatial_frequency)) if self.spatial_frequency.is_integer() \
            else str(self.spatial_frequency)

        if self.angle == 0:
            angle_text = ""
        elif self.angle > 0:
            angle_text = f"+{int(self.angle)}" if self.angle.is_integer() else f"+{self.angle}"
        else:
            angle_text = f"{int(self.angle)}" if self.angle.is_integer() else f"{self.angle}"

        return f"sin(2π*x*cos({spatial_frequency_text})*y{angle_text})\n"

    def get_wave(self, size):
        """
        Generates the waveform of the 2D sine wave.

        Parameters:
            size (int): The size of the square grid to generate the waveform.

        Returns:
            numpy.ndarray: The waveform of the 2D sine wave.
        """
        values = np.arange(size)
        x, y = np.meshgrid(values, values)

        return np.sin(
            2 * np.pi * (x * np.cos(np.deg2rad(self.angle)) * self.spatial_frequency +
                         y * np.sin(np.deg2rad(self.angle)) * self.spatial_frequency) / size
        )
