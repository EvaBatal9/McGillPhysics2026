import numpy as np
#from audiopressure import Duck_pressure, Cat_pressure, Cow_pressure, Dog_pressure, Donkey_pressure, Kathy_pressure, Lion_pressure, Monkey_pressure, Pig_pressure
from FFTstandard_freq import animals

pressures=[]
times=[]

for animal in animals:
    time,pressure=animal.unpackedPressure
    times.append(time)
    pressures.append(pressure)

'''time1, Duck_pressure = Duck_pressure
time2, Cat_pressure = Cat_pressure
time3, Cow_pressure = Cow_pressure
time4, Dog_pressure = Dog_pressure
time5, Donkey_pressure = Donkey_pressure
time6, Kathy_pressure = Kathy_pressure
time7, Lion_pressure = Lion_pressure
time8, Monkey_pressure = Monkey_pressure
time9, Pig_pressure = Pig_pressure'''

Time = times[7]

def evening_out(pressure_array):
    if len(pressure_array) < 117306:
        padding_length = 117306 - len(pressure_array)
        padding = np.zeros(padding_length)
        pressure_array = np.concatenate((pressure_array, padding))
    return pressure_array

foo=[]
location=(1,2)
for i in range(len(animals)):
    pres=animals[i].maze[location[1]][location[2]]*evening_out(pressures[i])
    foo.append(pres)

#master_pressure_array = np.array([k_Duck * evening_out(Duck_pressure), k_Cat * evening_out(Cat_pressure), k_Cow * evening_out(Cow_pressure), k_Dog * evening_out(Dog_pressure), k_Donkey * evening_out(Donkey_pressure), k_Kathy * evening_out(Kathy_pressure), k_Lion * evening_out(Lion_pressure), k_Monkey * evening_out(Monkey_pressure), k_Pig * evening_out(Pig_pressure)])

master_pressure_array=np.array(foo)
jumbled_pressure = np.sum(master_pressure_array, axis=0)
print(jumbled_pressure)