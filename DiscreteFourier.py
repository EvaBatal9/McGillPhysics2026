import math
import cmath


sound_wave = [0.012, -0.018, 0.025, -0.031, 0.040,
    -0.022, 0.015, -0.009, 0.003, 0.017,
    -0.028, 0.034, -0.041, 0.050, -0.037]

n_start = 0
N =  len(sound_wave)
# ,
    #0.029, -0.020, 0.011, -0.006, 0.002,
    #0.019, -0.027, 0.036, -0.044, 0.052,
    #-0.039, 0.030, -0.021, 0.014, -0.008
k = 0

x = 0
j = cmath.sqrt(-1)
total = 0

for k in range(N):
    total = 0
    n = n_start
    for n in range(N):
        x = sound_wave[n] * cmath.exp((-1j * 2 * math.pi * k * n)/ N)
        total += x
    print(total, "for frequency", k)

    


