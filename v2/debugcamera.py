
from ipdb import set_trace as idebug
import matplotlib.pyplot as plt 
import transforms as tf
import numpy as np 

import camera 
import thing 

class ThingViewer:
    def __init__(self, th:thing.Thing, cam: camera.Camera):
        self.th = th 
        self.cam = cam 

    #@profile
    def show(self):
        pix_coords = self.cam.computePixelCoordsForThing(self.th)

        self.plot_view(pix_coords)
        plt.xlabel("col")
        plt.ylabel("row")


    #   @profile
    def plot_view(self, pix_coords):
        #TODO Make a get polygon function 
        col, row = 0, 1
        # plt.plot(pix_coords[:,col], pix_coords[:,row], 'ko')

        #Each facet should get it's own segment. This is close enough
        segments = pix_coords[self.th.edges].reshape(-1, 1, 4)[:,:, :2].reshape(-1, 2)

        from  matplotlib.collections import LineCollection
        coll = LineCollection([segments], colors='k')
        plt.gca().add_collection(coll)



class DummyLens:
    pass 

import render 
import readobj 
import time
def main():
    # th = thing.make_example_thing()
    fn = "../data/models_resources/Xwing_0_0.obj"
    th = readobj.read_points(fn)
    cam = camera.Camera(camera.BaseLens(), 400, 400, 40)
    # renderer = render.WireframeMplRender()
    renderer = render.PolygonMplRender()


    viewer = ThingViewer(th, cam)

    ang = np.radians(40)
    th.state = [40,0,0, 0, np.pi/4, -3*np.pi/4]
    # th.state = [40,0,0, 0, 0,0]
    # cam.state = np.array([0,0,0, ang, 0, 0])  #Rotates wrong way?
    # cam.state = np.array([0,0,0, 0, -ang, 0])  #Rotates wrong way?
    # cam.state = np.array([0,0,0, 0, 0, ang])  #Rotates right way?

    # Draw once    
    # plt.clf()
    # pix_coords = cam.computePixelCoordsForThing(th)
    # renderer.paint(th, pix_coords)
    # plt.axis([0, cam.ncols, 0, cam.nrows])

    # plt.xlim(0,400)
    # plt.ylim(0,400)

    plt.clf()
    i = 0
    while True :
        # th.state[-1] += np.radians(4)
        th.state[-1] += np.radians(2)

        ang =  np.radians(30) * np.sin(2*np.pi*i/200.)
        # th.state[-2] = ang
        cam.state[0] = 10 * np.sin(2*np.pi*i/100)
        plt.clf()
        t0 = time.time()
        pix_coords = cam.computePixelCoordsForThing(th)

        #Filter on zmin/zmax 
        #Filter on col row outside of screen
        #Filter on normal vector direction
        #Filter on polygon size 

        renderer.paint(th, pix_coords)

        plt.axis([0, cam.ncols, 0, cam.nrows])
        print(1/(time.time() - t0))
        plt.pause(.01)
        # return
        
        i += 1


if __name__ == "__main__":
    main()