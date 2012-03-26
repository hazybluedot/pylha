#!/usr/bin/env python2

import numpy as np
from sys import stdout,stderr,argv
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import lha_sensor as ta

verbose=False
animate=False
val=0

stderr.write("%d\n" % len(argv))
if len(argv) == 2:
    val = float(argv[1])

def gauss(x,mu,sigma):
    return 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (x - mu)**2 / (2 * sigma**2) )

def plot_distribution(val):
    theta = np.pi/2*val
    sense = ta.lha_sensor()
    sigma = sense.get_sigma(100, theta)
    s = sense.sample_from(100, theta, 1000)

    x=None
    layers=160
    for n in range(-layers,layers):
        y=np.arange((2*n-1)*np.pi/2,(2*n+1)*np.pi/2,np.pi/256)[0:256]
        if verbose:
            stderr.write("layer %d: shape: %r\n" % (n,y.shape))
        if x==None:
            x = y
        else:
            if n != 0:
                y = y[::-1]
            x = np.vstack((x,y))

    ax=x[layers,:]

    f=gauss(x,theta,sigma)

    host = host_subplot(111)
    n=0
    plt.plot(ax,f[n+layers,:],linewidth=1, color='r', label='Gaussian assumption')
#plt.plot(ax,f[1,:],linewidth=1, color='r')
    plt.plot(ax,f.sum(axis=0),linewidth=1, color='b', linestyle='--', label='effective')
#ax.set_ticks([0., .5*np.pi, np.pi, 1.5*np.pi, 2*np.pi])
    plt.axvline(-np.pi/2, color='grey', linestyle='--')
    plt.axvline(np.pi/2, color='grey', linestyle='--')
    plt.axhline(1/np.pi, color='grey', linestyle=':', label='Uniform')
    plt.legend(loc=10)

    return plt

if animate:
    ims = []
    for val in np.arange(150):
        dec = float(val)/150
        fig = plt.figure("frame %f" % dec)
        plt = plot_distribution(dec)
    #ims.append(plt)
        plt.savefig("/tmp/frame_%f.png" % dec)
else:
    fig = plt.figure("frame %f" % val)
    plt = plot_distribution(val)
    plt.savefig(stdout,format='svg')

#import matplotlib.animation as animation
#im_ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=3000, blit=True)

#plt.savefig(stdout,format='svg')
#plt.show()
