import scipy.fft as sp
from jumblesignals import jumbled_pressure, Time
from FFTstandard_freq import animals
import matplotlib.pyplot as plt
import numpy as np


time_step = int(len(Time) / 26.6)

k = 0
i = time_step

while i <= len(Time):
    #everything from k = 0 to time_step is the first interval
    #then k += time step, i += timestep
    #then repeat until i = len(Time)
      
    current_time_array = Time[k:i]
    current_pressure_array = jumbled_pressure[k:i]

    N = len(current_pressure_array)
    dt = current_time_array[1] - current_time_array[0]
    freqs = sp.fftfreq(N, dt)

    fft_vals = sp.fft(current_pressure_array)
    magnitude = np.abs(fft_vals)

    positive = freqs > 0

    plt.figure(figsize=(10,4))
    plt.xlim(0,5000)
    plt.plot(freqs[positive], magnitude[positive])
    plt.title("Total Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

    k += time_step
    i += time_step

    for name in animals:
        target_freq = animals[name][2]
        idx = np.argmin(np.abs(freqs - target_freq))
        amplitude = magnitude[idx]
        print(f"{name}: {amplitude}")


    #pseudo code for what's going on:
    #we have the amplitude per frequency graph for the active time interval we are in, 
    # we see what the amplitude is for each of the animals IDs, 
    # and then we associate an amplitude to each animal