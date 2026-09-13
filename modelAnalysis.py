import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from tkinter import filedialog as dialog
import os
import matplotlib as mpl
from matplotlib import animation


datetime_filename = dialog.askopenfilename(title="Open Date and Time file")  # creates a dialog to choose the files where the date and time data is stored
neededdata_filename = dialog.askopenfilename(title="Open Needed Data file")  # creates a dialog to choose the files where the needed data (properties) is stored
angtens_filename = dialog.askopenfilename(title="Open Angular Data file")  # creates a dialog to choose the files where the angular data is stored

current_datetime = np.load(datetime_filename)  # load the date and time from the file
current_datetime = str(current_datetime)  # change the date and time to a string

J, k, B, T, limit, lol, step, spread, lop = np.load(neededdata_filename)  # Load the needed data (properties) from the file
limit = int(limit)  # convert limit to integer
lol = int(lol)  # convert the frame number to integer
step = int(step)  # convert the step number to integer

angtens = np.load(angtens_filename)  # load the angular data from the file
colang = np.cos(2*angtens)  # calculate cos(2*angle) for every element

x = np.arange(0, limit)  # sets up x range
y = np.arange(0, limit)  # sets up y range
X, Y = np.meshgrid(x, y)  # sets up grid of the x and y values to plot them

scale = 1  # sets a scale for the arrows
angx = scale * np.cos(angtens)  # calculates the u vector amount (for when doing smaller scale tests using arrows)
angy = scale * np.sin(angtens)  # calculates the v vector amount (for when doing smaller scale tests using arrows)

fig, ax = plt.subplots(1, 1) # initial set up for plot
R = ax.pcolormesh(X, Y, colang[:, :, 0], cmap='cividis', shading='gouraud', alpha=1)  # starts plotting the colour contour plot
Q = ax.quiver(X, Y, angx[:, :, 0], angy[:, :, 0], pivot='mid', color='k', units='inches', angles='uv', alpha=0)  # plots the vector plot (when needed)
ax.xaxis.set_ticklabels([])  # gets rid of the tick labels
ax.yaxis.set_ticklabels([])  # gets rid of the tick labels
ax.xaxis.set_ticks([])  # gets rid of the ticks
ax.yaxis.set_ticks([])  # gets rid of the ticks
ax.set_xlim(-1, limit)  # sets the x limits
ax.set_ylim(-1, limit)  # sets the y limits
fig.set_size_inches(8, 8)  # sets the size of the figure
ax.axis('square')  # equalises the aspect on each side

pbar = tqdm(total=(lol + 1))  # initialises the progress bar


def update_quiver(num, Q, X, Y):  # updates the vector plot and colour contour plot
    R.set_array(colang[:, :, num].ravel())  # sets the contour plot for that iteration
    U = angx[:, :, num]  # gets the U values for the vector plot for that iteration
    V = angy[:, :, num]  # gets the V values for the vector plot for that iteration
    Q.set_UVC(U, V)  # sets the vector plot for that iteration
    pbar.update(1)  # updates the progress bar
    return Q,

anim = animation.FuncAnimation(fig, update_quiver, frames=lol, fargs=(Q, X, Y), interval=0.1, blit=False, repeat=False) # creates the animation function
video_filename = os.getcwd() + r'\Videos\AFMrun2_size-' + str(limit) + '_10xspread-' + str(10*spread) + '_frames-' + str(lol) + '_stepchanges-' + str(step) + '_' + current_datetime # sets up the video filename
anim.save(video_filename + '.mp4', fps=60, extra_args=['-vcodec', 'libx264'], savefig_kwargs={'pad_inches': 1})  # saves the animation function to an mp4

mpl.use("pgf")  # sets up mpl and to use latex
mpl.rcParams['font.size'] = 18
mpl.rcParams["savefig.format"] = 'pdf'
style = {
        "pgf.texsystem": "pdflatex",
        "text.usetex": True,
        "pgf.preamble": [
         r"\usepackage[utf8x]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         r"\usepackage{cmbright}",
         ]
        }
mpl.rcParams.update(style)

avgturn = np.mean(colang, axis=(0, 1))  # calculates the mean of cos(2*angle).
x = np.arange(0, 15000)/(60*3)  # sets up the values for the x-axis

fig2, ax2 = plt.subplots(1, 1)  # initialises the plot
ax2.plot(x, avgturn, 'k-')  # plots the data
ax2.set_xlabel('Time into Animation (s)')  # labels the x-axis
ax2.set_ylabel(r'Mean Value of $\cos\left(2 \cdot \theta\right)$')  # labels the y-axis
fig2.set_size_inches(12, 9)  # sets the size of the figure
graph_filename = os.getcwd() + r'\Graphs\AFMrun2_size-' + f'{limit}_10xspread-{10*spread}_frames-{lol}_stepchanges-{step}' + current_datetime  # sets up the graph filename
fig2.savefig(graph_filename + '.pdf')  # saves the graph