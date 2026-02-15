import numpy as np
import librosa # type: ignore
from pathlib import Path

def getRms(animals):
    files=['audiofiles/Duckquack.mp3','audiofiles/Cat.mp3','audiofiles/Cow.mp3','audiofiles/Dog.mp3','audiofiles/Donkey.mp3','audiofiles/Kathy.mp3','audiofiles/Lion.mp3','audiofiles/Monkey.mp3','audiofiles/Pig.mp3']
    for i in range(len(files)):
        Amplitude, sr = librosa.load(files[i], sr=None)
        Amplitude_rms = np.sqrt(np.mean(Amplitude**2))
        animals[i].rms=Amplitude_rms


def array_sr_function(file_path):
    Amplitude, sr = librosa.load(file_path, sr=None)
    
    duration = len(Amplitude)/sr
    time = np.arange(len(Amplitude))/sr

    #taking the average (weird but you need to square, sum then sqrt, cause shit cancels out)
    Amplitude_rms = np.sqrt(np.mean(Amplitude**2))

    #conversion to pressure
    p0 = 2e-5  # Pascals
    target_spl = 60  # dB
    #converting 60dB to pascals
    target_prms = p0 * 10**(target_spl / 20)
    #finding the scale factor
    scale_factor = target_prms / Amplitude_rms
    #associating each amplitude value in y to pressure using scale factor
    pressure = Amplitude * scale_factor
    print("time length: ", len(time), "pressure length: ", len(pressure) )
    return time, pressure

Duck_pressure = array_sr_function('audiofiles/Duckquack.mp3')
Cat_pressure = array_sr_function('audiofiles/Cat.mp3')
Cow_pressure = array_sr_function('audiofiles/Cow.mp3')
Dog_pressure = array_sr_function('audiofiles/Dog.mp3')
Donkey_pressure = array_sr_function('audiofiles/Donkey.mp3')
Kathy_pressure = array_sr_function('audiofiles/Kathy.mp3')
Lion_pressure = array_sr_function('audiofiles/Lion.mp3')
Monkey_pressure = array_sr_function('audiofiles/Monkey.mp3')
Pig_pressure = array_sr_function('audiofiles/Pig.mp3')

