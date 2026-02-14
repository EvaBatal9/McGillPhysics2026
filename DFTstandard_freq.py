import numpy as np
import scipy.fft as sp
from DiscreteFourier import DFT
from audiopressure import Duck_pressure, Cat_pressure, Cow_pressure, Dog_pressure, Donkey_pressure, Kathy_pressure, Lion_pressure, Monkey_pressure, Pig_pressure

#unpacking pressure tuples into arrays
time, duck_pressure = Duck_pressure
time, Cat_pressure = Cat_pressure
time, Cow_pressure = Cow_pressure
time, Dog_pressure = Dog_pressure
time, Donkey_pressure = Donkey_pressure
time, Kathy_pressure = Kathy_pressure
time, Lion_pressure = Lion_pressure
time, Monkey_pressure = Monkey_pressure
time, Pig_pressure = Pig_pressure

#using scipy fft to convert to frequency domain (it is now pressure over frequency)
Duck_fft = DFT(duck_pressure)
Cat_fft = DFT(Cat_pressure)
Cow_fft = DFT(Cow_pressure)
Dog_fft = DFT(Dog_pressure)
Donkey_fft = DFT(Donkey_pressure)
Kathy_fft = DFT(Kathy_pressure)
Lion_fft = DFT(Lion_pressure)
Monkey_fft = DFT(Monkey_pressure)
Pig_fft = DFT(Pig_pressure)


print(Duck_fft[10000:10010])
