
from ipdb import set_trace as idebug
import matplotlib.pyplot as plt 
import transforms as tf
import numpy as np 

import camera 
import thing 
import shade


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
    shader = shade.AmbientLightShader()



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
    #The world.py loop
    while True :
        #Move object and camera 
        # th.state[-1] += np.radians(4)
        th.state[-1] += np.radians(2)

        ang =  np.radians(30) * np.sin(2*np.pi*i/200.)
        # th.state[-2] = ang
        cam.state[0] = 10 * np.sin(2*np.pi*i/100)

        
        plt.clf()
        t0 = time.time()
        #Compute relevant coordinates for thing for this camera
        pix_coords = cam.computePixelCoordsForThing(th)
        normals = cam.computeNormalsForThing(th)  #in camera's coord system

        # if cam.isOffScreen(pix_coords):
        #     continue 

        #Filter polygons to just the ones we want to render
        idx = np.ones(len(pix_coords), dtype=bool)
        idx &= cam.polyIsOnScreen(cam, pix_coords)
        idx &= polyFacesCamera(normals)
        idx &= polyIsLargeEnoughToRender(pix_coords)
        if np.sum(idx) == 0:
            continue 
        
        #Display the displayable polygons
        colours = shader.shade(th, pix_coords, normals, idx)
        renderer.paint(pix_coords[idx], th.edges[idx], colours)

        plt.axis([0, cam.ncols, 0, cam.nrows])
        print(1/(time.time() - t0))
        plt.pause(.01)
        # return
        
        i += 1


def polyFacesCamera(cam, normals):
    mat = cam.getAttitudeVector()
    costheta = np.dot(normals, mat)
    return costheta < 0

    return np.ones(len(normals), dtype=bool)

def polyIsLargeEnoughToRender(pix_coords):
    cmin = pix_coords[:, :, 0].min(axis=1)
    cmax = pix_coords[:, :, 0].max(axis=1)
    rmin = pix_coords[:, :, 0].min(axis=1)
    rmax = pix_coords[:, :, 0].max(axis=1)

    minAreaToRender_pix = 2  #TODO: make this an argument?
    area = (cmax - cmin) * (rmax - rmin)
    return area > minAreaToRender_pix


if __name__ == "__main__":
    main()