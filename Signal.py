import numpy as np

""" Class responsible for storing data about each sinusoidal signal """


class Signal:
    def __init__(self, amplitude, frequency, phase):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def signal_to_text(self):
        """ generate information about signal and returns it as string """
        amplitude_text = str(self.amplitude)
        frequency_text = str(self.frequency)
        phase_text = str(self.phase)
        return f"{amplitude_text} sin(2π*{frequency_text}*t+{phase_text})\n"

    def get_sine_wave(self, time):
        """ generates sine function from stored data and time axis """
        return self.amplitude * np.sin(2 * np.pi * self.frequency * time + np.deg2rad(self.phase))
