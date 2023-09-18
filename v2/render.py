
from matplotlib.collections import LineCollection, PolyCollection
from ipdb import set_trace as idebug
import matplotlib.pyplot as plt 
import transforms as tf
import numpy as np 

import camera 
import thing 

class AbstractRender:
    def paint(self, th:thing.Thing, coords:np.ndarray):
        raise NotImplementedError("Don't call baseclass directly") 


class PointCloudMplRender(AbstractRender):
    def paint(self, th, coords):
        plt.plot(coords[:,0], coords[:,1], 'k.')


class WireframeMplRender(AbstractRender):
    def paint(self, th, pix_coords):
        col, row = 1, 2

        segments = pix_coords[th.edges].reshape(-1, 1, 4)[:,:, :2].reshape(-1, 2)
        coll = LineCollection([segments], colors='k')
        plt.gca().add_collection(coll)
        plt.axis('equal')

def lmap(function, *array):
    return list(map(function, *array))


class PolygonMplRender(AbstractRender):
    def paint(self, th:thing.Thing, pix_coords):

        #TODO
        #Filter on norm pointing toward camera
        idx = np.ones(len(th.edges), dtype=bool)

        polys = pix_coords[th.edges[idx]]

        
        #Painter's algorithm. Sort in decreasing zorder
        zorder = polys[:,:,2].mean(axis=1)
        srt = np.argsort(zorder)[::-1]
        polys = polys[srt, :,:]
        colours = th.colours[srt]

        #Reshape to a list of arrays for PolyCollection
        polys = lmap(lambda x: x.reshape(-1, 4), polys)
        polys = lmap(lambda x: x[:,:2], polys)  #Strip z and w coords 

        coll = PolyCollection(polys, closed=False, facecolors=colours)

        plt.gca().add_collection(coll)
        plt.plot([0,1], [0,1], 'k-')
        plt.axis('equal')


