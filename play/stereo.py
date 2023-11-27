
#Draw two different views of the same object.
#Is it like watching a 3d movie?
#Not so far.

from ipdb import set_trace as idebug
import matplotlib.pyplot as plt 
import numpy as np 
import readobj 
import world 
import camera
import shade
import thing 
import render 


def main():
    fn = "../data/models_resources/Xwing_0_0.obj"
    th = readobj.read_points(fn)
    th.state = np.array([80,-7, 0,0, .5,np.pi/2], dtype=float)

    bbox1 = camera.Bbox(0, 0, 400, 400)
    cam1 = camera.Camera(camera.BaseLens(), bbox1, 20)
    cam1.state[1] = +12

    bbox2 = camera.Bbox(0, 400, 400, 400)
    cam2 = camera.Camera(camera.BaseLens(), bbox2, 20)
    cam1.state[1] = -12

    shader = shade.AmbientLightShader()
    renderer = render.PolygonMplRender() 
    wrld = world.World(renderer, shader, [th], [cam2, cam1])

    i=0
    while True:
        i+=1 
        th.state[-1] = np.fmod(np.radians(i), 360)
        plt.cla()
        wrld.advance(1)
        plt.axis([0, 800, 400, 0])
        plt.axis('off')
        plt.pause(.1)
        # return 
    plt.clf()
    wrld.advance(0)
    plt.axis([0, 400, 0, 800])