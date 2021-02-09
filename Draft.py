import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.constants as spc
import os

mpl.rcParams['text.usetex'] = True 
mpl.rcParams['text.latex.preamble'] = [r'\usepackage[cm]{sfmath}', r'\usepackage{braket}']
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'cm'
mpl.rcParams['font.size'] = 27
mpl.rcParams["savefig.format"] = 'eps'

# Use os.getcwd() to get the folder you're in atm

grid = np.zeros((9,9))
