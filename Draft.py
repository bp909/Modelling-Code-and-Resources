import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.constants as spc
import os
from matplotlib import animation

mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage[cm]{sfmath}', r'\usepackage{braket}']
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'cm'
mpl.rcParams['font.size'] = 27
mpl.rcParams["savefig.format"] = 'eps'

# Use os.getcwd() to get the folder you're in atm



def exchange(J,s1,s2):
	spprod = np.cos(s2-s1)# (s1-s2) #*(spc.hbar**2)
	Eex=-J*spprod

	return Eex

def anis(k,th):
	Ek = -k*(np.sin(th))**2

	return Ek

def diff(Eb,Ea):
	delE = Eb-Ea
	print(str(delE))
	return delE

def Prob(dE,T):
	p=np.exp(-dE/(T*spc.k))
	print(str(p))
	test = np.random.random()
	if test < p:
		return 1
	else:
		return 0

J=-100
k=2
T = 10
limit = 11
lol = 500

anggrid = 2*np.pi*np.random.random((limit,limit)) - np.pi
#spingrid = np.random.randint(0,2, size=(limit,limit)) - 0.5
angtens = np.zeros((limit,limit,lol))
for j in range(0, lol):
	for h in range(0, limit**2):
		locr = np.random.randint(1,limit-1)
		locc = np.random.randint(1,limit-1)
	
		exchangelist = np.zeros((4))
		for i in range(0,4):
			if (i % 2) == 0:
				exchangelist[i] = exchange(J, anggrid[locr,locc], anggrid[locr+(i-1),locc])
			else:
				exchangelist[i] = exchange(J, anggrid[locr,locc], anggrid[locr,locc+(i-2)])
		
		an = anis(k, anggrid[locr,locc])
		Es = an + np.sum(exchangelist)
		
		randturn = 2*np.pi*np.random.normal(0,0.1) #- np.pi*0.2
		
		exchangelist2 = np.zeros((4))
		for i in range(0,4):
			if (i % 2) == 0:
				exchangelist2[i] = exchange(J, (anggrid[locr,locc]+randturn), anggrid[locr+(i-1),locc])
			else:
				exchangelist2[i] = exchange(J, (anggrid[locr,locc]+randturn), anggrid[locr,locc+(i-2)])
	
		an2 = anis(k, (anggrid[locr,locc]+randturn))

		Ef = an2 + np.sum(exchangelist2)
	
		delE = diff(Es,Ef)
	
		turn = Prob(delE,T)
	
		if turn == 1:
			anggrid[locr,locc] = anggrid[locr,locc] + randturn
		else:
			pass
	angtens[:,:,j] = anggrid


accangtens = angtens[1:(limit-1), 1:(limit-1), :]

X, Y = np.meshgrid(np.arange(0,9), np.arange(0,9))

scale = 1

angx = scale*np.cos(accangtens)
angy = scale*np.sin(accangtens)

fig, ax = plt.subplots(1,1)
Q = ax.quiver(X, Y, angx[:,:,0], angy[:,:,0], pivot='mid', color='k', units='inches')

ax.set_xlim(-1, 9)
ax.set_ylim(-1, 9)

def update_quiver(num, Q, X, Y):
	
	U = angx[:, :, num]
	V = angy[:, :, num]
	Q.set_UVC(U, V)
	
	if round(100*num/lol, 2) % 1 == 0:
		print(str(round(100*num/lol, 0)) + '%')
	else:
		pass
	
	return Q,

# you need to set blit=False, or the first set of arrows never gets
# cleared on subsequent frames
anim = animation.FuncAnimation(fig, update_quiver, frames=lol, fargs=(Q, X, Y), interval=1, blit=False)

anim.save(os.getcwd() + r'\AFM3.mp4', fps=60, extra_args=['-vcodec', 'libx264'], savefig_kwargs={'pad_inches':1})




