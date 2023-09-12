import matplotlib.pyplot as plt 
import numpy as np 


class Backend():
    """
    TODO
    1. A backend should know screen size in pixels
    2. Need a pygame backend
    3. Pass in properties, not just colour
    """

    def __init__(self, ncols, nrows):
        self.ncols = ncols 
        self.nrows = nrows 

    def wireframe(self, vertices, clr):
        """Plot object in wireframe
        
        Inputs
        ----------
        vertices
            (3x2 numpy array) of pixel
            coordinates of a single facet
        clr
            Colour code of facet
        """
        raise NotImplementedError("Base class is Abstract")

    def patch(self, vertices, clr):
        """Plot facet as a solid colour
        
        Inputs
        ----------
        vertices
            (3x2 numpy array) of pixel
            coordinates of a single facet
        clr
            Colour code of facet
        """
        raise NotImplementedError("Base class is Abstract")

    def mark_centroids(self, vertices, zdist, label):
        """Mark centroid of a facet
        
        Inputs
        ----------
        vertices
            (3x2 numpy array) of of pixel
            coordinates of a single facet
        clr
            Colour code of facet
        """
        raise NotImplementedError("Base class is Abstract")


class MplBackend(Backend):
    """Docstrings in base class """
    def wireframe(self, vertices, clr):
        for i in range(len(vertices)):
            x = vertices[ [0,1,2,0], 0]
            y = vertices[ [0,1,2,0], 1]
            plt.plot( x, y, '-', color=clr )


    def patch(self, vertices, clr):
        patch = plt.Polygon(vertices, color=clr, ec='k', lw=.1)
        # patch = plt.Polygon(vertices, color=clr)
        plt.gca().add_patch(patch)
        pass


    def mark_centroids(self, vertices, zdist, clr):
        assert vertices.shape == (3,2)
        cent = np.sum(vertices, axis=0) / 3
        assert cent.shape == (2,)
        plt.plot(cent[0], cent[1], 'k.')
        plt.text(cent[0], cent[1], " %s %.4f" %(clr, zdist))
