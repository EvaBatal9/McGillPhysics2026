import scipy.fft as sp
from jumblesignals import jumbled_pressure, Time
from FFTstandard_freq import animals
import matplotlib.pyplot as plt
import numpy as np


time_step = int(len(Time) / 26.6)

k = 0
i = time_step

while i <= len(Time):
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




    #everything from k = 0 to time_step is the first interval
    #then k += time step, i += timestep
    #then repeat until i = len(Time)











"""
def matchfrequency(animal_fft):
    i = 0
    counter = 0
    n = 0
    while i <= len(frequency_total):
        if animal_fft[i] == frequency_total[i+n]:
           counter += 1
        else:
            n+=1    
        i += 1
    
    if counter == len(animal_fft):
        return True
    else:
        return False

"""
