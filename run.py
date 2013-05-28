import sys

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from Reader import Reader
from Body import Vector

def sim(bodies, dt = 60, T = 3600 * 24, plot = False, savedir = None):
    fignum = 0
    t = 0
    while t <= T:
        for i, b in enumerate(bodies):
            b.a = Vector(0, 0, 0)
            for other in bodies[i + 1:]:
                f = b.force(other)
                b.a += f / b.m
                other.a -= f / other.m
            
        for b in bodies:
            b.step(dt)
        t += dt

        if plot:
            fig = plt.figure()
            axes = Axes3D(fig)
            for b in bodies:
                b.plot(axes)
            plt.savefig('{0}{1:05.0f}.png'.format(savedir, fignum))
            plt.close('all')
            fignum += 1
            
            

if __name__ == '__main__':
    reader = Reader(sys.argv[1])
    bodies = reader.getBodies()
    fig = plt.figure()
    sim(bodies, dt = 1, T = 3600, plot = True, savedir = sys.argv[2])
