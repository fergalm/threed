import matplotlib.pyplot as plt
from ipdb import set_trace as idebug
import numpy as np

from backend import MplBackend
from engine import Engine
from camera import Camera
import sprite




def interact():
    obj = Sprite()
    camera = Camera(MplBackend())

    i = 827
    plt.clf()

    while True:
        plt.cla()
        obj.setAttitude_rad( np.radians([i, 0, 0]))
        camera.renderSingleSprite(obj)

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
    camera = Camera(5e+2)
    backend = MplBackend(800, 600)
    engine = Engine(camera, backend)
    obj = sprite.Pyramid()

    plt.clf()
    i = 0
    while True:
    # for i in range(270):
    # for i in [199]:
        plt.cla()

        obj.setAttitude_rad( np.radians([0,0,i]))
        # camera.pos = np.array([0, 0, 4-i/8, 1])
        # obj.pos = [1 + .01*i, 0, -1 + .01*i]
        engine.renderSingleSprite(obj)

        tpi =  .5
        # plt.axis('equal')
        plt.axis([0, 800, 0, 600])
        # plt.axis([-tpi, tpi, -tpi, tpi])
        # plt.axis([2, 10, -4, 4])
        # plt.axis([3, 7, -6, 6])
        plt.title(i)
        plt.pause(.05)
        # return 
        i += 1