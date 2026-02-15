import scipy.fft as sp
from jumblesignals import jumbled_pressure
from FFTstandard_freq import Duck_fft, Cat_fft, Cow_fft, Dog_fft, Donkey_fft, Kathy_fft, Lion_fft, Monkey_fft, Pig_fft

frequency_total = sp.fft(jumbled_pressure)
  
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
    
print(matchfrequency(Duck_fft))


"""
