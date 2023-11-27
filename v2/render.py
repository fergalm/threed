
from matplotlib.collections import LineCollection, PolyCollection
from ipdb import set_trace as idebug
import matplotlib.pyplot as plt 
import numpy as np 

from . import thing 

def lmap(function, *array):
    return list(map(function, *array))


class AbstractRender:
    def paint(self, th:thing.Thing, coords:np.ndarray):
        raise NotImplementedError("Don't call baseclass directly") 


class PointCloudMplRender(AbstractRender):
    def paint(self, polys, colours):
        coords = polys[:,:,:2].reshape(-1, 2)
        plt.cla()
        plt.plot(coords[:,0], coords[:,1], 'k.')


class WireframeMplRender(AbstractRender):
    def paint(self, polys, colours):
        # segments = pix_coords[th.edges].reshape(-1, 1, 4)[:,:, :2].reshape(-1, 2)
        segments = polys.reshape(-1, 1, 4)[:,:,:2].reshape(-1, 2)
        coll = LineCollection([segments], colors='k')
        plt.cla()
        plt.gca().add_collection(coll)
        # plt.axis('equal')



class PolygonMplRender(AbstractRender):
    def paint(self, polys, colours):
        
        #Painter's algorithm. Sort in decreasing zorder
        zorder = polys[:,:,2].mean(axis=1)
        srt = np.argsort(zorder)[::-1]
        polys = polys[srt, :,:]
        colours = colours[srt]

        #Reshape to a list of arrays for PolyCollection
        polys = lmap(lambda x: x.reshape(-1, 4), polys)
        polys = lmap(lambda x: x[:,:2], polys)  #Strip z and w coords 

        coll = PolyCollection(polys, closed=False, facecolors=colours)

        # plt.cla()
        plt.gca().add_collection(coll)
        plt.plot([0,1], [0,1], 'k-')



class NumberedPolygonRender(PolygonMplRender):
    def paint(self, polys, colours):
        PolygonMplRender.paint(self, polys, colours)

        # segments = polys.reshape(-1, 1, 4)[:,:,:2].reshape(-1, 2)
        # coll = LineCollection([segments], colors='k')
        # plt.gca().add_collection(coll)

        centx = polys[:, :, 0].mean(axis=1)
        centy = polys[:, :, 1].mean(axis=1)
        zorder = polys[:, :, 1].mean(axis=1)

        import frmplots.plots as fplots 
        outline = fplots.outline()
        for col, row, z, clr in zip(centx, centy, zorder, colours):
            plt.plot(col, row, 'o', mec='k', color=clr)
            plt.text(col, row, "%.1f" %(z), color='w', path_effects=outline)

        srt = np.argsort(zorder)[::-1]
        print(zorder[srt])
        print(colours[srt]) 


import matplotlib.patches as mpatch 
import frmplots.plots as fplots 
class DebugPolygonRender(AbstractRender):
    def paint(self, polys, colours, pix_coords):
        zorder = polys[:,:,2].mean(axis=1)
        srt = np.argsort(zorder)[::-1]
        polys = polys[srt, :,:]
        colours = colours[srt]

        #Reshape to a list of arrays for PolyCollection
        polys = lmap(lambda x: x.reshape(-1, 4), polys)
        polys = lmap(lambda x: x[:,:2], polys)  #Strip z and w coords 

        plt.cla()
        plt.plot([0,1], [0,1], 'k-')
        plt.axis([0,400, 400, 0])
        ax = plt.gca()
        for i in range(len(polys)):
            patch = mpatch.Polygon(polys[i], closed=False, fc=colours[i])
            ax.add_patch(patch)

            col = polys[i][:,0].mean()
            row = polys[i][:,1].mean()
            z = zorder[srt[i]]
            plt.plot(col, row, 'o', mec='k', color=colours[i])
            plt.text(col, row, "%.3f" %(z), color='w', path_effects=fplots.outline())

        print(pix_coords)




# class PolygonNormalRender(AbstractRender):
#     def paint(self, polys, colours):
#         coll = self.drawPolygons(polys, colours)
#         vecs = self.drawNormals(polys, colours)
#         plt.cla()
#         plt.gca().add_collection(coll)
#         plt.gca().add_collection(vecs)
#         plt.plot([0,1], [0,1], 'k-')

#     def drawNormals(self, polys, colours):
#         ... 


#     def drawPolygons(self, polys, colours):
#         #Painter's algorithm. Sort in decreasing zorder
#         zorder = polys[:,:,2].mean(axis=1)
#         srt = np.argsort(zorder)[::-1]
#         polys = polys[srt, :,:]
#         colours = colours[srt]

#         #Reshape to a list of arrays for PolyCollection
#         polys = lmap(lambda x: x.reshape(-1, 4), polys)
#         polys = lmap(lambda x: x[:,:2], polys)  #Strip z and w coords 

#         #Show polygons 
#         coll = PolyCollection(polys, closed=False, facecolors=colours)
#         return coll 

