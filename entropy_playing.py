from rythm import complex_entropy
import matplotlib.pyplot as plt
import numpy as np
import os


def gauss(x, mu, sigma):
     return np.exp( - (x - mu)**2 / (2 * sigma**2) )
print(os.listdir('techno'))
x = np.linspace(-1, 1, 1000)
sigmas = np.linspace(0.1, 1, 10)
for sigma in sigmas:
     dist = gauss(x, 0, sigma)
     dist = dist/np.sum(dist)
     plt.plot(x, dist, ) 
     print(complex_entropy(dist))

plt.show()
