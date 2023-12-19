from scipy.fft import fft, ifft, fftfreq
import numpy as np
import matplotlib.pyplot as plt

fs = 10
N = 20
t = np.arange(0, (N - 1) / fs, 0.001)
ts = np.arange(0, N / fs, 1 / fs)
signal = 5 * np.sin(2 * np.pi * 10 * t)
signal_s = 5 * np.sin(2 * np.pi * 10 * ts)
fft_x_axis = fftfreq(len(signal_s), 1 / fs)
X = fft(signal_s)

# Correct subplot creation
plt.subplot(3, 1, 1)
plt.stem(ts, signal_s)
plt.plot(t, signal)  # Use t instead of ts here
plt.subplot(3, 1, 2)
plt.stem(fft_x_axis, abs(X))
plt.subplot(3, 1, 3)
plt.stem(ts, np.real(ifft(X)))
plt.show()
