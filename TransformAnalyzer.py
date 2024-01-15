from scipy.fft import fft, ifft, dct, idct

""" Class responsible for performing FFT, IFFT, DCT, IDCT operations on given function """


class TransformAnalyzer:
    def __init__(self, signal):
        """ signal is a function operations will be performed on """
        self.signal = signal

    def calculate_fft(self):
        """ Perform FFT on the signal and return the result """
        fft_data = fft(self.signal)
        return fft_data

    def calculate_ifft(self):
        """ Perform IFFT on the given FFT function and return the result """
        ifft_data = ifft(self.signal)
        return ifft_data

    def calculate_dct(self):
        """ Create an AxisHandler instance to generate frequency axis
            Perform DCT on the signal with normalization and return the result """
        dct_data = dct(self.signal, norm='ortho')
        return dct_data

    def calculate_idct(self):
        """ Perform IDCT on the given DCT function with normalization and return the result """
        idct_data = idct(self.signal, norm='ortho')
        return idct_data
