from scipy.fft import fftfreq
import numpy as np

""" Class responsible for generating OX axis for plotting """


class AxisHandler:
    def __init__(self, data):
        """ data is a dictionary that contains information about parameters
            required to generate time and frequency axis """
        self.samples_number = data['samples_number']
        self.sampling_frequency = data['sampling_frequency']
        self.time_step = data['time_step']

    def generate_time_axis(self):
        """ calculates time axis from data and returns it as vector """
        time_axis = np.arange(0, self.samples_number / self.sampling_frequency, self.time_step)
        return time_axis

    def generate_discrete_time_axis(self):
        """ calculates discrete time axis and returns it as a vector """
        discrete_time_axis = np.linspace(0, self.samples_number / self.sampling_frequency, self.samples_number)
        return discrete_time_axis

    def generate_frequency_axis(self):
        """ calculates frequency axis for plotting DFT and DCT and returns it as a vector """
        fft_x_axis = fftfreq(self.samples_number, d=1 / self.sampling_frequency)
        return fft_x_axis
