from ipdb import set_trace as idebug

import numpy as np 

from . import transforms as tf 
from .detector import Detector
from .lens import BaseLens 
from .thing import Thing 

"""
Local Coordinates of vertices relative to centre of object 
World Coords of vertices relative to centre of the universe 
Rel   Coords in the world relative to the camera's position 
View  Coords relative to the viewing plane of the camera.
Screen Coords on the screen. Units are pixels. (0,0) at top left
        of screen. col increases to the right, row increases down.
        dist increases for objects further in the background

"""


    


class BaseCamera:
    """
    The camera maps the location of a Thing from world coordinates to screen coordinates

    The class itself converts from world coordinates to relative coordinates,
    then passes the rest of the job to the lens and detector.

    Although this class exposes a lot of its implementation for inspection,
    the only two public functions you should be using outside of debugging are 

    * `computePixelCoordsForThing()`
    * `computeNormalsForThing()`
    """
    def __init__(self, lens:BaseLens, detector:Detector):
        self.lens = lens 
        
        self.col0 = detector.woffset
        self.row0 = detector.hoffset
        self.ncols = detector.width
        self.nrows = detector.height
        self.horizontal_fov_rad = np.radians(detector.horz_fov_degrees)
        # self.vertical_fov_rad = self.horizontal_fov_rad * nrows / ncols 
        self.plate_scale_rad_per_pixel = self.horizontal_fov_rad / float(self.ncols)

        self.state = np.array([0,0,0, 0,0,0], dtype=float)

        self.minDistToRender = 1 
        """Don't render objects tha are too close to the camera"""
        self.maxDistToRender = 1000
        """Don't render objects too far away from the camera"""

    # def getFrame(self):
    #     left = self.col0 
    #     right = left + self.ncols 
    #     top = self.row0 
    #     bottom = top + self.nrows 
    #     return [left, right, bottom, top]


    def computeNormalsForThing(self, th:Thing):
        """Compute the normal vectors for the facets of a Thing in World coordinates

        Inputs
        ------------
        * th
            * A single Thing object 
        
            
        Returns 
        ---------
        A `n x 3` array, where `n` is the number of facets in the Thing. The columns
        represent the x, y, and z components of the normal vectors
        """

        localToWorld = th.getLocalToWorldMat()
        worldToView = self.getWorldToViewMat()
        mat = localToWorld @ worldToView
        mat = localToWorld

        #Trim off w coord. Not needed for normals 
        mat = mat[:3, :3]
        # normals = np.dot(th.norms, mat)
        normals = th.norms @ mat
        return normals 
    
    def computePixelCoordsForThing(self, th:Thing):
        """Compute screen coordinates of the vertices of a Thing

        Inputs
        ------------
        * th
            * A single Thing object 

        Returns
        ----------
        An `n x 3` array of coordinates, where `n` is the number of vertices in the
        Thing. Units are pixels. The columns are col, row, and distance 

        """
        localToWorld = th.getLocalToWorldMat()
        worldToView = self.getWorldToViewMat()
        # mat = np.dot(localToWorld, worldToView)
        mat = localToWorld @ worldToView

        #Compute transformation matrix from local to view coords
        # view_coords = np.dot(th.vertices, mat)
        view_coords = th.vertices @ mat

        #USe lens to covert view coords to degrees and distance 
        ang_coords_rad = self.lens.getAngularCoords_rad(view_coords)

        screen_coords_pix = self.convertAngularToScreenCoords(ang_coords_rad)
        return screen_coords_pix

    def getAttitudeVector(self):
        """Get the unit vector pointing toward centre of FOV in world coords
        
        Returns
        ------------
        A `1 x 4` array of coordinates 

        Note
        -------
        This explicitly assumes camera is pointing along +ve x-axis
        in local coordinates
        """
        mat = self.getWorldToRelMat()
        vec = np.array([1,0,0,0])
        return vec @ mat

    def getWorldToViewMat(self):
        """
        The the transformation matrix from world coordinates to
        view coordinates, i.e coordaintes relative to the imaging plane. The convention is
        that the camera is looking along the x-axis, with z pointing "up"

        Returns
        ---------
        A `4 x 4` matrix
        """
        mat1 = self.getWorldToRelMat()
        mat2 = self.getRelToViewCoords()
        return mat1 @ mat2
    
    def getWorldToRelMat(self):
        """
        Get the matrix that transforms world coordinates to relativate coordinates
        (i.e coordinates relative to the camera).

        In the abscence of any rotation of the camera, this matrix
        just subtracts the camera coordinates from the Thing coordinates.
        If the camera has been rotated, the impact of that rotation
        is also taken into account (e.g if the camera is pointed "backwards"
        it can see "behind" itself. 

        Notes
        ------
        This is the camera view, so we do things opposite 
        to the usual way. If the camera moves to the right,
        the objects relative coordinates move to the left.
        If the camera pitches up, the relative coordinates move down.

        Also, we reverse the order of transformations. Translate
        first, then rotate
        
        Returns
        ---------
        A `4 x 4` matrix
        """

        x, y, z, rho, theta, phi = -1 * self.state 
            
        zmat = tf.rotateAboutZ(phi)
        ymat = tf.rotateAboutY(theta)
        xmat = tf.rotateAboutX(rho)
        tmat = tf.translateMat([x, y, z])
        mat = tmat @ xmat @ ymat @ zmat 
        return mat 

    def getRelToViewCoords(self):
        """
        Create a matrix that converts relative coordinates to view coordinates.

        Relative coords are the position of the Thing relative to the camera,
        view coordinates are those relative to the imaging plane. 

        Convention is that camera lens points in +x direction with +z
        corresponding to up, and +y to left. This matrix converts
        those coordinates to (horzizontal, vertical, and distance)
        coordinates.

        * Horizontal == -y 
        * Vertical == +z 
        * Distance == +x 

        Returns
        ---------
        A `4 x 4` matrix

        """

        mat = np.zeros((4,4))
        mat[0, 2] = +1
        mat[1, 0] = -1
        mat[2, 1] = +1
        mat[3, 3] = +1  #Keep the w coord unchanged 
        return mat 

    def convertAngularToScreenCoords(self, ang_coords_rad):
        """Convert coordinates in radians from point of view
        to pixels.

        We convert radians to pixels using the platescale, then offset
        the results so that (0,0) in angular coords corresponds to
        the centre of the screen

        Remember (0,0) in pixel coords is the top left of the screen
        so +ve vertical coords are toward the top of the screen and 
        -ve vertical coords are toward the bottom

        Note that the resulting screen coords need not be on
        the screen. Some additional filtering might be required

        Inputs
        --------
        ang_coords_rad 
            An `n x 3` array, where `n` is the number of vertices,
            and the columns are horizontal distance (radians),
            verticle distance (radians), and distance along the 
            line of sight. 
            
        Returns
        ---------
        An `n x 3` array, where `n == len(ang_coords_rad)`
        
        """
        col_pix = ang_coords_rad[:,0] / self.plate_scale_rad_per_pixel
        col_pix += .5 * self.ncols
        col_pix += self.col0

        row_pix = .5 * self.nrows 
        row_pix -= ang_coords_rad[:,1] / self.plate_scale_rad_per_pixel
        row_pix += self.row0 

        out = np.empty_like(ang_coords_rad)
        out[:,0] = col_pix 
        out[:,1] = row_pix 
        out[:,2] = ang_coords_rad[:,2]
        return out 

    def filterPolyForOnScreen(self, poly_coords):
        """Check which polygons are on-screen


        Inputs
        -----------

        
                TODO
        -----
        Should this belong to the detetor class?

        """
        assert poly_coords.ndim == 3 

        cmin = poly_coords[:, :, 0].min(axis=1)
        cmax = poly_coords[:, :, 0].max(axis=1)
        rmin = poly_coords[:, :, 1].min(axis=1)
        rmax = poly_coords[:, :, 1].max(axis=1)
        zmin = poly_coords[:, :, 2].min(axis=1)
        zmax = poly_coords[:, :, 2].max(axis=1)
        assert cmin.ndim == 1
        assert len(cmin) == len(poly_coords)

        idx =  (cmax > 0) & (cmin < self.ncols)
        idx &= (rmax > 0) & (rmin < self.nrows)
        idx &= (zmin > self.minDistToRender) & (zmax < self.maxDistToRender)
        return idx 





class Camera(BaseCamera):
    """A default camera, with reasonable settings"""
    def __init__(self):
        lens  = BaseLens()
        detector = Detector(0,0, 800, 600, 3600)
        BaseCamera.__init__(self, lens, detector)