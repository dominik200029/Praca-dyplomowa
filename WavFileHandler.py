from scipy.io import wavfile
import numpy as np


# WavFileHandler class handles reading audio data from a WAV file
class WavFileHandler:
    def __init__(self, file):
        self.file = file

    def get_audio_data(self):
        # Read the WAV file and return time axis and audio data
        sampling_rate, data = wavfile.read(self.file)
        duration = len(data) / sampling_rate
        time_axis = np.linspace(0, duration, len(data))
        return data, time_axis, sampling_rate
