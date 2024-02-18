from abc import ABC, abstractmethod
import numpy as np


class GaussianFilter(ABC):
    def __init__(self, x_cord, y_cord, cut_off_frequency):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.cut_off_frequency = cut_off_frequency

    @abstractmethod
    def apply(self):
        pass


class LowPassGaussianFilter(GaussianFilter):
    def __init__(self, x_cord, y_cord, cut_off_frequency):
        super().__init__(x_cord, y_cord, cut_off_frequency)

    def apply(self):
        mask = ((np.exp(-(self.x_cord ** 2 + self.y_cord ** 2) / (2 * self.cut_off_frequency ** 2)))
                / (2 * np.pi * self.cut_off_frequency ** 2))
        return mask


class HighPassGaussianFilter(GaussianFilter):
    def __init__(self, x_cord, y_cord, cut_off_frequency):
        super().__init__(x_cord, y_cord, cut_off_frequency)

    def apply(self):
        mask = ((1 - np.exp(-(self.x_cord ** 2 + self.y_cord ** 2) / (2 * self.cut_off_frequency ** 2)))
                / (2 * np.pi * self.cut_off_frequency ** 2))
        return mask
