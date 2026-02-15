import numpy as np
import scipy.fft as sp
import matplotlib.pyplot as plt
from audiopressure import Duck_pressure, Cat_pressure, Cow_pressure, Dog_pressure, Donkey_pressure, Kathy_pressure, Lion_pressure, Monkey_pressure, Pig_pressure

animals = {
    "Duck": Duck_pressure,
    "Cat": Cat_pressure,
    "Cow": Cow_pressure,
    "Dog": Dog_pressure,
    "Donkey": Donkey_pressure,
    "Kathy": Kathy_pressure,
    "Lion": Lion_pressure,
    "Monkey": Monkey_pressure,
    "Pig": Pig_pressure
}

for name, data in animals.items():
    time, pressure = data

    N = len(pressure)
    dt = time[1] - time[0]
    freqs = sp.fftfreq(N, dt)

    fft_vals = sp.fft(pressure)
    magnitude = np.abs(fft_vals)

    positive = freqs > 0

    ID = freqs[np.argmax(magnitude[positive])]

    mean_freq = np.sum(freqs[positive] * magnitude[positive]) / np.sum(magnitude[positive])

    mean_pressure = np.avg(pressure)

    animals[name] = (time, pressure, ID, mean_freq, mean_pressure)

