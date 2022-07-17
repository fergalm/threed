import matplotlib.pyplot as plt
from ipdb import set_trace as idebug
import numpy as np

from camera import Camera
from sprite import Sprite




def interact():
    obj = Sprite()
    camera = Camera()

    i = 827
    plt.clf()

    while True:
        plt.cla()
        obj.setAttitude_rad( np.radians([i, 0, 0]))
        camera.renderShape(obj)

        plt.plot([0,1], [0,1], 'k-')
        # plt.axis([-2,2,-2,2])
        plt.title(i)
        plt.pause(.05)
        char = input()

        if char == 'n':
            i+=1
        elif char == 'b':
            i-=1


def main():
    obj = Sprite()
    camera = Camera()

    plt.clf()
    i = 0
    while True:
    # for i in range(270):
    # for i in [199]:
        plt.cla()

        obj.setAttitude_rad( np.radians([i, i, 0]))
        val = camera.renderShape(obj)
        if val == 1:
            return 
        # camera.renderEnvelope(obj)

        tpi =  .5
        # plt.axis('equal')
        plt.axis([-tpi, tpi, -tpi, tpi])
        # plt.axis([2, 10, -4, 4])
        # plt.axis([3, 7, -6, 6])
        plt.title(i)
        plt.pause(.05)
        # return 
        i += 1