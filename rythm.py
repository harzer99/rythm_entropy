import scipy as sc
import numpy as np
import pydub
import soundfile as sf
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
from multiprocessing.pool import Pool

def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return np.float32(y) / 2**15, a.frame_rate
    else:
        return y, a.frame_rate
    
def rythm_entropy(audio, sr, start = 0.1,  cutoff = 4):
    transformed = np.fft.rfft(audio)
    cutoff_index = int(cutoff/sr*len(audio))
    start_index = int(start/sr*len(audio))
    transformed = transformed[start_index:cutoff_index]
    normalization = np.abs(np.sum(transformed))
    entropy = complex_entropy(transformed/normalization)
    return entropy

def complex_entropy(transformed):
    p = np.abs(transformed)
    #plt.plot(p)
    #plt.show()
    S = -np.sum(p*(np.log(p)))
    print(S)
    return S

def analyze_file(path):
    audio, sr = read(path)
    audio = np.mean(audio, axis = 1)
    return rythm_entropy(audio, sr)

def analyze_folder(path):
    entropies = {}
    for file_name in os.listdir(path):
        entropies[file_name] = analyze_file(path+ '/'+ file_name)
        
    return entropies

if __name__ == '__main__':
    complex_music = analyze_folder('complex_music')
    techno = analyze_folder('techno')

    print(complex_music)
    print(techno)
