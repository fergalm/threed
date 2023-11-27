
from ipdb import set_trace as idebug
import matplotlib.pyplot as plt 
import numpy as np 

from . import transforms as tf
from . import thing 

class ThingViewer:
    def __init__(self, th:thing.Thing):
        self.th = th 

    def show(self):
        mat = self.th.getLocalToWorldMat()
        vertices = np.dot(self.th.vertices, mat)

        grid = plt.gcf().subplot_mosaic("ab\n.d")

        grid['a'].sharey( grid['b'])
        grid['d'].sharex( grid['b'])

        plt.sca(grid['a'])
        self.plot_view(vertices, 1, 2)
        plt.xlabel("Y")
        plt.ylabel("Z")
        plt.ylim(-2, 2)

        plt.sca(grid['b'])
        plt.cla()
        self.plot_view(vertices, 0, 2)
        # plt.axis('equal')

        plt.sca(grid['d'])
        plt.cla()
        self.plot_view(vertices, 0, 1)
        plt.xlabel("X")
        plt.axis('equal')
        plt.xlim(-2, 2)


    def plot_view(self, vertices, col, row):
        #TODO Make a get polygon function 
        plt.plot(vertices[:,col], vertices[:,row], 'ko')
        for i in range(self.th.numEdges):
            ed = self.th.edges[i] 
            clr = self.th.colours[i]
            for j in range(len(ed)):
                k = (j+1) % 3
                p1 = vertices[ed[j]]
                p2 = vertices[ed[k]]
                plt.plot([ p1[col], p2[col]], [p1[row], p2[row]], '-', color=clr)


import time
def main():
    th = thing.make_example_thing()

    viewer = ThingViewer(th)
    viewer.show()
    print(th.norms)


    # plt.clf()
    # i = 0
    # while True:
    #     th.state[-1] = np.radians(i)
    #     th.state[-3] = np.radians(i)
    #     th.state[0] = 2 * np.sin(2 * np.pi * i/40)
    #     plt.clf()
    #     t0 = time.time()
    #     viewer.show()
    #     print(1/(time.time() - t0 - .1))
    #     plt.pause(.1)
    #     i += 1
