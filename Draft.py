import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.constants as spc

mpl.rcParams['text.usetex'] = True 
mpl.rcParams['text.latex.preamble'] = [r'\usepackage[cm]{sfmath}', r'\usepackage{braket}']
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'cm'
mpl.rcParams['font.size'] = 27
mpl.rcParams["savefig.format"] = 'eps'

grid = np.zeros((9,9))
t = np.linspace(0,4,100)
y = np.sin(2*np.pi*t)
plt.plot(t,y)
plt.show()