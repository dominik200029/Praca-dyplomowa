import numpy as np

from WavFileHandler import WavFileHandler
from Signal import Signal

""" Class responsible for generating waves from signals """


class SignalsHandler:
    def __init__(self):
        """
        signals - list that stores Signal objects
        signal_amount - a number of signals already stored in signals list
        signals_labels - list that stores signals as strings
        """
        self.signals = []
        self.signals_labels = []
        self.signal_amount = 0

    def append_signal(self, signal: Signal):
        """ takes Signal object and adds it to signals lists, incrementing the number of signals stored by 1 """
        self.signals.append(signal)
        self.signals_labels.append(signal.signal_to_text())
        self.signal_amount += 1

    def generate_wave(self, time_axis, discrete_time_axis):
        """ taking time axis and discrete time axis  vectors to generate sinusoidal waves from all signals stored
            in signals list """
        wave = np.zeros(len(time_axis))  # initialize wave vector with zeros
        sampled_wave = np.zeros(len(discrete_time_axis))  # initialize sampled_wave vector with zeros

        for signal in self.signals:
            wave += signal.get_sine_wave(time_axis)
            sampled_wave += signal.get_sine_wave(discrete_time_axis)
        return wave, sampled_wave

    @staticmethod
    def generate_wave_from_file(file):
        """ generate wave, it's time axis and sampling frequency of a signal stored in .wav file """
        file_handler = WavFileHandler(file)
        data, time_axis, sampling_frequency = file_handler.get_audio_data()
        return data, time_axis, sampling_frequency
