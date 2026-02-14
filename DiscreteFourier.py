import math
import cmath


def DFT(pressure_wave):
    pressure = [] 
    n_start = 0
    N =  len(pressure_wave)
    k = 0
    x = 0
    j = cmath.sqrt(-1)
    total = 0

    for k in range(N):
        total = 0
        n = n_start
        for n in range(N):
            x = pressure_wave[n] * cmath.exp((-1j * 2 * math.pi * k * n)/ N)
            total += x
        pressure.append(total)
        

        


