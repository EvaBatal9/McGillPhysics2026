import numpy as np
import scipy.fft as sp
import matplotlib.pyplot as plt
from audiopressure import Duck_pressure, Cat_pressure, Cow_pressure, Dog_pressure, Donkey_pressure, Kathy_pressure, Lion_pressure, Monkey_pressure, Pig_pressure
from mazeTest import animals

for animal in animals:
    print(animal.maze)

#unpacking pressure tuples into arrays
time, Duck_pressure = Duck_pressure
time, Cat_pressure = Cat_pressure
time, Cow_pressure = Cow_pressure
time, Dog_pressure = Dog_pressure
time, Donkey_pressure = Donkey_pressure
time, Kathy_pressure = Kathy_pressure
time, Lion_pressure = Lion_pressure
time, Monkey_pressure = Monkey_pressure
time, Pig_pressure = Pig_pressure

#using scipy fft to convert to frequency domain (it is now pressure over frequency)
Duck_fft = sp.fft(Duck_pressure)
Cat_fft = sp.fft(Cat_pressure)
Cow_fft = sp.fft(Cow_pressure)
Dog_fft = sp.fft(Dog_pressure)
Donkey_fft = sp.fft(Donkey_pressure)
Kathy_fft = sp.fft(Kathy_pressure)
Lion_fft = sp.fft(Lion_pressure)
Monkey_fft = sp.fft(Monkey_pressure)
Pig_fft = sp.fft(Pig_pressure)
