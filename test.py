from scipy.fft import dct
import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0, 0.1, 0.001)
signal = 5 * np.sin(2 * np.pi * 10 * t)

dct_signal = dct(signal)

# Correct subplot creation
plt.subplot(2, 1, 1)
plt.plot(t, signal)
plt.subplot(2, 1, 2)
plt.stem(dct_signal)
plt.show()
