import numpy as np
from tqdm import tqdm
import os
import time

def exchange(J, s1, s2):  # function that calculates the exchange energy contribution between two spins
    spprod = np.cos(s2 - s1)  # dot product of the spins
    Eex = -J * spprod  # exchange energy calculation
    return Eex


def anis(k, th):  # function that calculates the anisotropic energy of a spin
    Ek = -k * (np.sin(th)) ** 2  # anisotropic energy calculation
    return Ek


def diff(Eb, Ea):  # function that calculates difference in energy between the
    delE = Eb - Ea  # difference calculation
    return delE


def Prob(dE, T):  # function that decides whether that specific spin can change to it's new position
    kb = 1  # boltzman constant is 1 for this scale
    p = np.exp(-dE / (T * kb))  # uses the boltzmann distribution to calculate the probability that the spin changes
    test = np.random.random()  # generates a random number between 0 and 1 to decide whether to turn the spin
    if test < p:  # returns a 1 if the spin will turn on that condition, 0 if not
        return 1
    else:
        return 0



J = 100  # exchange energy scale factor
k = 2  # anisotropic energy scale factor
B = 10000000  # old and unused, kept for consistency of saved data
T = 10  # temperature simulated at
limit = 100  # size of simulation (100x100)
lol = 500  # number of frames of animation
step = int(np.around((limit ** 2), 0))  # number of spins to look at changing in one frame
spread = 0.1  # old and unused, kept for consistency of saved data
lop = 50  # old and unused, kept for consistency of saved data

anggrid = 2 * np.pi * np.random.random((limit, limit)) - np.pi  # generates the random grid of angles needed
angtens = np.zeros((limit, limit, lol))  # contains the history of the anggrid to save it
delE = np.zeros((lol, step))  # keeps change in energy in grid (originally needed for monitoring)
turn = np.zeros((lol, step))  # keeps turn in grid (originally needed for monitoring)

for j in tqdm(range(0, lol)):  # loop for each frame
    for h in range(0, step):  # loop for each change in each frame
        locr = np.random.randint(0, limit)  # chooses a random row for the spin
        locc = np.random.randint(0, limit)  # chooses a random column for the spin
        exchangelist = np.zeros((4))  # sets up place to store exchange energy values from each of the four spin exchange interactions
        for i in range(0, 4):  # goes through the four closest spins to the current spin to calculate the exchange energy
            if (i % 2) == 0:  # checks if number is even, easy way to get it to check both up/down and left/right
                exchangelist[i] = exchange(J, anggrid[locr, locc], anggrid[((locr + (i - 1)) % limit), (locc % limit)])  # the two spins go into this to have there exchange energy calculated
            else:
                exchangelist[i] = exchange(J, anggrid[locr, locc], anggrid[(locr % limit), ((locc + (i - 2)) % limit)])  # the two spins go into this to have there exchange energy calculated

        an = anis(k, anggrid[locr, locc])  # calculates the anisotropic energy contribution
        Es = an + np.sum(exchangelist)  # sums the total exchange energy and anisotropic energy
        randturn = 2 * np.pi * np.random.random()  # calculates a random turn for to see if the spin wants to turn that much
        exchangelist2 = np.zeros((4))  # same as prior exchange list
        for i in range(0, 4):  # loops through neighbouring spins with this new angular position
            if (i % 2) == 0:
                exchangelist2[i] = exchange(J, (anggrid[locr, locc] + randturn), anggrid[((locr + (i - 1)) % limit), (locc % limit)])
            else:
                exchangelist2[i] = exchange(J, (anggrid[locr, locc] + randturn), anggrid[(locr % limit), ((locc + (i - 2)) % limit)])

        an2 = anis(k, (anggrid[locr, locc] + randturn))  # calculates the anisotropic energy for this new angular position
        Ef = an2 + np.sum(exchangelist2)  # sums the total exchange energy and anisotropic energy for the new angular position
        delE[j, h] = diff(Es, Ef)  # calculates the difference in energy between the old and new angular positions
        turn[j, h] = Prob(delE[j, h], T)  # decides whether the spin will turn to the new angular position
        if turn[j, h] == 1:  # performs the turn if previous line returns a 1
            anggrid[locr, locc] = anggrid[locr, locc] + randturn
        else:
            pass

    angtens[:, :, j] = anggrid  # saves the current position of the angular grid


current_datetime = time.strftime("%Y-%m-%d_%H-%M-%S")  # produces the current date and time (so names don't conflict)
np.save(os.getcwd() + '\Data\AFMrunangular' + current_datetime, angtens)  # saves that angular position through time in a file
np.save(os.getcwd() + '\Data\AFMdatetime' + current_datetime, current_datetime)  # saves the date and time produced (so we can match the names)
needed_data = [J, k, B, T, limit, lol, step, spread, lop]  # puts the needed parameters together
np.save(os.getcwd() + '\Data\AFMneededdata' + current_datetime, needed_data)  # saves the needed parameters to a file

