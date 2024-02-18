import numpy as np


class LowPassFilter:
    def __init__(self, cut_off_frequency):
        self.cut_off_frequency = cut_off_frequency

    def apply(self, values):
        indices_to_zero = np.where(np.abs(values) > self.cut_off_frequency)
        return indices_to_zero


class HighPassFilter(LowPassFilter):
    def __init__(self, cut_off_frequency):
        super().__init__(cut_off_frequency)

    def apply(self, values):
        indices_to_zero = np.where(np.abs(values) < self.cut_off_frequency)
        return indices_to_zero


class BandPassFilter:
    def __init__(self, low_cut_off_frequency, high_cut_off_frequency):
        self.low_cut_off_frequency = low_cut_off_frequency
        self.high_cut_off_frequency = high_cut_off_frequency

    def apply(self, values):
        indices_to_zero = (
                (np.abs(values) < self.low_cut_off_frequency)
                | (np.abs(values) > self.high_cut_off_frequency)
        )
        return indices_to_zero


class BandStopFilter(BandPassFilter):
    def __init__(self, low_cut_off_frequency, high_cut_off_frequency):
        super().__init__(low_cut_off_frequency, high_cut_off_frequency)

    def apply(self, values):
        indices_to_zero = (
                (self.low_cut_off_frequency < np.abs(values))
                & (np.abs(values) < self.high_cut_off_frequency)
        )
        return indices_to_zero
