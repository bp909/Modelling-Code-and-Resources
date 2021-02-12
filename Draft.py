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



def exchange(J,s1,s2):
    if s1 == s2:
        spprod = 0.25*spc.hbar**2
    else:
        spprod = -0.75*spc.hbar**2
    Eex=-J*spprod
    return Eex

def anis(k,th):
    Ek = -k*(np.sin(th))**2
    return Ek

def diff(Eb,Ea):
    delE = Eb-Ea
    return delE

def Prob(dE,T):
    P=np.exp(-dE/(spc.k*T))
    test = np.random.random()
    if test < P:
        return 1
    else:
        return 0

J=50
k=1
T = 1
limit = 9
lol = limit**2

anggrid = 2*np.pi*np.random.random((limit,limit))
spingrid = np.random.randint(0,2, size=(limit,limit)) - 0.5

locr = np.random.randint(1,limit-1)
locc = np.random.randint(1,limit-1)

exchangelist = np.zeros((4))
for i in range(0,4):
    if (i % 2) == 0:
        exchangelist[i] = exchange(J, spingrid[locr,locc], spingrid[locr+(i-1),locc])
    else:
        exchangelist[i] = exchange(J, spingrid[locr,locc], spingrid[locr,locc+(i-2)])

an = anis(k, anggrid[locr,locc])
Es = an + np.sum(exchangelist)

randturn = (2*np.pi*np.random.random()) % (2*np.pi)


exchangelist2 = np.zeros((4))
for i in range(0,4):
    if (i % 2) == 0:
        exchangelist2[i] = exchange(J, spingrid[locr,locc], spingrid[locr+(i-1),locc])
    else:
        exchangelist2[i] = exchange(J, spingrid[locr,locc], spingrid[locr,locc+(i-2)])

an2 = anis(k, anggrid[locr,locc])
Ef = an2 + np.sum(exchangelist2)

delE = diff(Es,Ef)

turn = Prob(delE,T)

if turn == 1:
    anggrid[locr,locc] = anggrid[locr,locc] + randturn
else:
    pass





